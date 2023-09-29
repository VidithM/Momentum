"""Add user mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ...database import users as sql_user

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_user(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a user."""
    async with info.context.db.acquire() as connection:
        await connection.begin()

        try:
            rid, _ = await sql_user.add(connection, parent, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await connection.rollback()
            raise

        await connection.commit()

        return rid


@_resolver.field("create_user")
async def create_user(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve add user."""
    try:
        rid = await _add_user(
            parent,
            info,
            input,
        )
    except Exception as err:
        return {
            "error": str(err),
        }

    return {"user": await sql_user.search_by_rids(info.context.db.cursor, info, [rid])}
