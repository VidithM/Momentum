"""Community resolver."""
import logging
from typing import Any, Dict, Optional, List

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts, users


logger = logging.getLogger(__name__)

_resolver = ObjectType("Community")

@_resolver.field("users")
async def resolve_users(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[List[Dict[str, Any]]]:
    """Get users information."""
    terms = {
        "rids": [parent["users"]]
    }
    print(terms)
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await users.search(
        cur,
        info,
        terms,
    )
    print(rids)
    return (await users.search_by_rids(cur, info, rids))


@_resolver.field("posts")
async def resolve_posts(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    print(parent)
    terms = {
        "communities": [parent["rid"]]
    }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await posts.search(
        cur,
        info,
        terms,
    )
    return (await posts.search_by_rids(cur, info, rids))
