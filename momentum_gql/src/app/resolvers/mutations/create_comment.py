"""Add comment mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import comments as sql_comment

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_comment(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a comment."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            rid, _ = await sql_comment.add(connection, parent, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise

        await info.context["db"].commit()

        return rid


@_resolver.field("create_comment")
async def create_comment(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve add comment."""
    rid = await _add_comment(
        parent,
        info,
        input,
    )
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    comment = await sql_comment.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"comment": comment[0]}
