"""Community resolver."""
import logging
from typing import Any, Dict, Optional, List

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp
import json

from ...database import posts


logger = logging.getLogger(__name__)

_resolver = ObjectType("Community")


@_resolver.field("users")
async def resolve_users(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[List[Dict[str, Any]]]:
    """Get users information."""
    print(parent)

    rid_str = []
    if parent.get("users"):
        for item in parent.get("users", []):
            rid_str.append(str(item))
    query = {"terms": rid_str}
    async with aiohttp.ClientSession() as session:
        url = "http://host.docker.internal:8080/getuser"
        response = await session.get(url, json=query)
        users = await response.json(content_type="application/json")
        user_dicts = []
        if users:
            for item in users:
                user = json.loads(item)
                user["rid"] = int(user["rid"])
                user_dicts.append(user)
    return user_dicts


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
