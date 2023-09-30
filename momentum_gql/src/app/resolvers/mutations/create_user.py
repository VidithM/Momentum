"""Add user mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import users as sql_user

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_user(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a user."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            rid, _ = await sql_user.add(connection, parent, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise

        await info.context["db"].commit()

        return rid


@_resolver.field("create_user")
async def create_user(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve add user."""
    print("Adding user")
    print(info.context["db"])
    # try:
    rid = await _add_user(
        parent,
        info,
        input,
    )
    # except Exception as err:
    #     return {
    #         "error": str(err),
    #     }
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    user = await sql_user.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"user": user[0]}
