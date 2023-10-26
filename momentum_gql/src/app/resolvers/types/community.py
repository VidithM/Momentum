"""Community resolver."""
import logging
from typing import Any, Dict, Optional, List

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts, users, user_community


logger = logging.getLogger(__name__)

_resolver = ObjectType("Community")


@_resolver.field("users")
async def resolve_users(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[List[Dict[str, Any]]]:
    """Get users information."""
    terms = {"community_ids": [parent["rid"]]}
    print(terms)
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await user_community.search_by_community_ids(
        cur,
        info,
        [parent["rid"]],
    )
    print(rids)
    if rids:
        return await users.search_by_rids(cur, info, rids)
    else:
        return None


@_resolver.field("posts")
async def resolve_posts(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    print(parent)
    terms = {"communities": [parent["rid"]]}
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await posts.search(
        cur,
        info,
        terms,
    )
    return await posts.search_by_rids(cur, info, rids)
