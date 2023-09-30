"""user mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import users as sql_user

logger = logging.getLogger(__name__)

_resolver = MutationType()

async def _update_user(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a user."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            await sql_user.update(connection, info, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise


        await info.context["db"].commit()
    return data["rid"]


@_resolver.field("update_user")
async def update_user(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update user."""
    rid = await _update_user(
        parent,
        info,
        input,
    )

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    user = await sql_user.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"user": user[0]}
