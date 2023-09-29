"""community mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ...database import communities as sql_community

logger = logging.getLogger(__name__)

_resolver = MutationType()

async def _update_community(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a community."""
    async with info.context.db.acquire() as connection:
        await connection.begin()

        try:
            await sql_community.update(connection, info, data)

        except Exception:
            logger.error("Rolling back update due to exception.")
            await connection.rollback()
            raise

        await connection.commit()
    return data["rid"]


@_resolver.field("update_community")
async def update_community(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update community."""
    try:
        rid = await _update_community(
            parent,
            info,
            input,
        )
    except Exception as err:
        return {
            "error": str(err),
        }

    return {"community": await sql_community.search_by_rids(info.context.db.cursor, info, [rid])}
