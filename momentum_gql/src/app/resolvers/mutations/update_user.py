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
        if data.get("communities"):
            for community in data["communities"]:
                comm_data = {}
                comm_data["user_id"] = data["rid"]
                comm_data["user_ids"] = [data["rid"]]
                comm_data["community_id"] = community
                comm_data["community_ids"] = [community]

                print(comm_data)
                rid = await ucomm.search(connection, _, comm_data)
                print(rid)
                if not rid:
                    try:
                        _, _ = await ucomm.add(connection, _, comm_data)
                    except Exception as exc:
                        logger.error("Rolling back update due to exception.")
                        logger.error(str(exc))
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
    print(user)
    return {"user": user[0]}
