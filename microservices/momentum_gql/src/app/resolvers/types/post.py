"""Posts resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp
import json
from ...database import comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Post")


@_resolver.field("community")
async def resolve_community(
    parent: Dict[str, Any],
    _info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get community information"""
    query = {"rid": parent["community"]}
    async with aiohttp.ClientSession() as session:
        url = "http://host.docker.internal:8011/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="application/json")
    return data["data"][0]


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
    terms = {"posts": [parent["rid"]]}
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            rids = await comments.search(
                cur,
                info,
                terms,
            )
            print(rids)
            if rids:
                print(await comments.search_by_rids(cur, info, rids))
                return await comments.search_by_rids(cur, info, rids)
            else:
                return None
