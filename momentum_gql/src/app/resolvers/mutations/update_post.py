"""post mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ...database import posts as sql_post

logger = logging.getLogger(__name__)

_resolver = MutationType()

async def _update_post(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a post."""
    async with info.context.db.acquire() as connection:
        await connection.begin()

        try:
            await sql_post.update(connection, info, data)

        except Exception:
            logger.error("Rolling back update due to exception.")
            await connection.rollback()
            raise

        await connection.commit()
    return data["rid"]


@_resolver.field("update_post")
async def update_post(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update post."""
    try:
        rid = await _update_post(
            parent,
            info,
            input,
        )
    except Exception as err:
        return {
            "error": str(err),
        }

    return {"post": await sql_post.search_by_rids(info.context.db.cursor, info, [rid])}
