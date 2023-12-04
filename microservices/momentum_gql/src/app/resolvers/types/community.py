"""Community resolver."""
import logging
from typing import Any, Dict, Optional, List

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp

from ...database import posts


logger = logging.getLogger(__name__)

_resolver = ObjectType("Community")


@_resolver.field("users")
async def resolve_users(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[List[Dict[str, Any]]]:
    """Get users information."""
    query = {"rids": parent["users"]}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8080/get"
        response = await session.get(url, json=query)
        users = await response.json(content_type="text/json")
    return {"users": users}


@_resolver.field("posts")
async def resolve_posts(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    print(parent)
    terms = {"communities": [parent["rid"]]}
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            rids = await posts.search(
                cur,
                info,
                terms,
            )
            if rids != []:
                return await posts.search_by_rids(cur, info, rids)
            else:
                return None
