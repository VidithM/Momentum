"""Posts resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp
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
        url = "http://localhost:8011/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="application/json")
    return data["data"][0]


@_resolver.field("user")
async def resolve_user(
    parent: Dict[str, Any],
    _info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get user information."""
    query = {"rid": [parent["community"]]}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8080/get"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"user": data[0]} or None


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
            if rids != 0:
                return await comments.search_by_rids(cur, info, rids)
            else:
                return None
