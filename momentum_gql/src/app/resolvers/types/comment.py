"""Comment resolver."""
import logging
from typing import Any, Dict, Optional

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts, users, comments

logger = logging.getLogger(__name__)

_resolver = ObjectType("Comment")


@_resolver.field("post")
async def resolve_post(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get post information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            post = await posts.search_by_rids(cur, info, [parent["post"]])
    return post[0]


@_resolver.field("user")
async def resolve_user(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get user information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            return (await users.search_by_rids(cur, info, [parent["user"]]))[0]


@_resolver.field("comments")
async def resolve_comments(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get comments information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            terms = {"parents": [parent["rid"]]}
            rids = await comments.search(
                cur,
                info,
                terms,
            )
            return await comments.search_by_rids(cur, info, rids)


@_resolver.field("parent")
async def resolve_comment(
    parent: Dict[str, Any],
    info: GraphQLResolveInfo,
) -> Optional[Dict[str, Any]]:
    """Get parent information."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            return (await comments.search_by_rids(cur, info, [parent["parent"]]))[0]
