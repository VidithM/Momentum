"""Comment resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...database import posts, users, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Comment")

@_resolver.field("post")
async def resolve_post(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get post information."""
    return await posts.search_by_rids(info.context.db.cursor, info, parent["post"])


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

@_resolver.field("parent")
async def resolve_comment(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get parent information."""
    return await comments.search_by_rids(info.context.db.cursor, info, parent["parent"])
