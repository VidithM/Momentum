"""User resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts, comments, communities

logger = logging.getLogger(__name__)

_resolver = ObjectType("User")

@_resolver.field("communities")
async def resolve_communities(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get communities information."""
    terms = {
        "rids": [parent["communities"]]
    }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await communities.search(
        cur,
        info,
        terms,
    )
    return (await communities.search_by_rids(cur, info, rids))


@_resolver.field("posts")
async def resolve_posts(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get posts information."""
    terms = {
        "users":[parent["rid"]]
    }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await posts.search(
        cur,
        info,
        terms,
    )
    return (await posts.search_by_rids(cur, info, rids))

@_resolver.field("comments")
async def resolve_comments(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    terms = {
        "users": [parent["rid"]]
    }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    rids = await comments.search(
        await cur,
        info,
        terms,
    )
    return (await comments.search_by_rids(cur, info, rids))
