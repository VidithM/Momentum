"""Comment resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp
import json

from ...database import posts, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Comment")


@_resolver.field("post")
async def resolve_post(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get post information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            post = await posts.search_by_rids(cur, info, [parent["post"]])
    return post[0] or None


@_resolver.field("user")
async def resolve_user(
    parent: Dict[str, Any],
    _info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get user information."""
    query = {"terms": [str(parent["user"])]}
    async with aiohttp.ClientSession() as session:
        url = "http://host.docker.internal:8080/getuser"
        response = await session.get(url, json=query)
        user = await response.json(content_type="application/json")
        user = json.loads(user[0])
        user["rid"] = int(user["rid"])
    return user


@_resolver.field("comments")
async def resolve_comments(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            terms = {"parents": [parent["rid"]]}
            rids = await comments.search(
                cur,
                info,
                terms,
            )
            if rids:
                return await comments.search_by_rids(cur, info, rids)
            return None


@_resolver.field("parent")
async def resolve_comment(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get parent information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            print(parent["parent"])
            parents = await comments.search_by_rids(cur, info, [parent["parent"]])
            if parents:
                return parents[0]
            else:
                return None
