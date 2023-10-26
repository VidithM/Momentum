"""user mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import users as sql_user
from ...database import user_community as ucomm

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _delete_user_community(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a user."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        for community in data["communities"]:
            comm_data = {}
            comm_data_s = {}
            comm_data["user_id"] = 0
            comm_data_s["user_ids"] = [data["rid"]]
            comm_data["community_id"] = 0
            comm_data_s["community_ids"] = [community]

            rid = await ucomm.search(connection, info, comm_data_s)
            comm_data["rid"] = rid
            print(comm_data)
            if rid is not None:
                try:
                    print("Deleting")
                    await ucomm.update(connection, info, comm_data)
                except Exception as exc:
                    logger.error("Rolling back update due to exception.")
                    logger.error(str(exc))
                    await info.context["db"].rollback()
                    raise

        await info.context["db"].commit()
    return data["rid"]


@_resolver.field("delete_user_community")
async def delete_user_community(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update user."""
    rid = await _delete_user_community(
        parent,
        info,
        input,
    )

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    user = await sql_user.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"user": user[0]}
