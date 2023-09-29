"""User resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from ...database import posts, comments, communities

logger = logging.getLogger(__name__)

_resolver = ObjectType("User")

@_resolver.field("communities")
async def resolve_communities(
    info: GraphQLResolveInfo,
    parent: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Get communities information."""
    terms = {
        "community": parent["rid"]
    }
    rids = await communities.search(
        info.context.db.cursor,
        info,
        terms,
    )
    return await communities.search_by_rids(info.context.db.cursor, info, rids)


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
