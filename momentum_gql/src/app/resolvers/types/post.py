"""Posts resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...database import communities, users, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Post")

@_resolver.field("community")
async def resolve_community(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get community information."""
    return await communities.search_by_rids(info.context.db.cursor, info, parent["community"])


@_resolver.field("user")
async def resolve_user(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get user information."""
    return await users.search_by_rids(info.context.db.cursor, info, [parent["user"]])

@_resolver.field("comments")
async def resolve_comments(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    terms = {
        "post": parent["rid"]
    }
    rids = await comments.search(
        info.context.db.cursor,
        info,
        terms,
    )
    return await comments.search_by_rids(info.context.db.cursor, info, rids)
