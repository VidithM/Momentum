"""community mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import communities as sql_community
from ...database import user_community as ucomm

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _delete_community_user(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a community."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()
        for user in data["users"]:
            comm_data = {}
            comm_data_s = {}
            comm_data["user_id"] = 0
            comm_data_s["user_ids"] = [user]
            comm_data["community_id"] = 0
            comm_data_s["community_ids"] = [data["rid"]]
            rid = await ucomm.search(connection, _, comm_data_s)
            comm_data["rid"] = rid
            print(comm_data)
            if rid is not None:
                try:
                    await ucomm.update(connection, _, comm_data)
                except Exception as exc:
                    logger.error("Rolling back update due to exception.")
                    logger.error(str(exc))
                    await info.context["db"].rollback()
                    raise
        await info.context["db"].commit()
    return data["rid"]


@_resolver.field("delete_community_user")
async def delete_community_user(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update community."""
    rid = await _delete_community_user(
        parent,
        info,
        input,
    )

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    community = await sql_community.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"community": community[0]}
