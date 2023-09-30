"""Posts resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import communities, users, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Post")

@_resolver.field("community")
async def resolve_community(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get community information."""
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    return (await communities.search_by_rids(cur, info, [parent["community"]]))[0]


@_resolver.field("user")
async def resolve_user(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get user information."""
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    return (await users.search_by_rids(cur, info, [parent["user"]]))[0]

@_resolver.field("comments")
async def resolve_comments(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    terms = {
        "posts": [parent["rid"]]
    }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await comments.search(
        cur,
        info,
        terms,
    )
    return (await comments.search_by_rids(cur, info, rids))
