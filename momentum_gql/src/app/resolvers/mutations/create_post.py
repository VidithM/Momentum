"""Add post mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts as sql_post

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_post(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a post."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            rid, _ = await sql_post.add(connection, parent, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise

        await info.context["db"].commit()

        return rid


@_resolver.field("create_post")
async def create_post(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve add post."""
    rid = await _add_post(
        parent,
        info,
        input,
    )

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    post = await sql_post.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"post": post[0]}