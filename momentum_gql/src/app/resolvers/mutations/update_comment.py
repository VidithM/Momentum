"""comment mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import comments as sql_comment

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _update_comment(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a comment."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # await connection.begin()

            try:
                await sql_comment.update(cur, info, data)
            except Exception:
                logger.error("Rolling back update due to exception.")
                await conn.rollback()
                raise

            await conn.commit()
    return data["rid"]


@_resolver.field("update_comment")
async def update_comment(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update comment."""
    try:
        rid = await _update_comment(
            parent,
            info,
            input,
        )
    except Exception as err:
        return {
            "error": str(err),
        }
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            comment = await sql_comment.search_by_rids(cur, info, [rid])
    return {"comment": comment[0]}
