"""Work Order resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...database import posts, users

logger = logging.getLogger(__name__)

_resolver = ObjectType("Community")

@_resolver.field("users")
async def resolve_users(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get users information."""
    terms = {
        "community": parent["rid"]
    }
    rids = await users.search(
        info.context.db.cursor,
        info,
        terms,
    )
    return await users.search_by_rids(info.context.db.cursor, info, rids)


@_resolver.field("posts")
async def resolve_posts(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    terms = {
        "community": parent["rid"]
    }
    rids = await posts.search(
        info.context.db.cursor,
        info,
        terms,
    )
    return await posts.search_by_rids(info.context.db.cursor, info, rids)
