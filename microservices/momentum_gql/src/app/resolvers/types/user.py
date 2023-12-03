"""User resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp

from ...database import posts, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("User")


@_resolver.field("communities")
async def resolve_communities(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get communities information."""
    query = {"users": parent["rid"]}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"community": data[0]} or None


@_resolver.field("posts")
async def resolve_posts(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    terms = {"users": [parent["rid"]]}
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            rids = await posts.search(
                cur,
                info,
                terms,
            )
            if rids != []:
                return await posts.search_by_rids(cur, info, rids)
            return None


@_resolver.field("comments")
async def resolve_comments(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    terms = {"users": [parent["rid"]]}
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            rids = await comments.search(
                await cur,
                info,
                terms,
            )
            if rids != []:
                return await comments.search_by_rids(cur, info, rids)
            else:
                return None
