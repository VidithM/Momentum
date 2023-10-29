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


async def _update_community(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a community."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # await connection.begin()

            try:
                await sql_community.update(cur, info, data)
            except Exception:
                logger.error("Rolling back update due to exception.")
                await info.context["db"].rollback()
                raise
            if data.get("users"):
                print(data["users"])
                for user in data["users"]:
                    comm_data = {}
                    comm_data["user_id"] = user
                    comm_data["user_ids"] = [user]
                    comm_data["community_id"] = data["rid"]
                    comm_data["community_ids"] = [data["rid"]]
                    rid = await ucomm.search(cur, _, comm_data)
                    if not rid:
                        try:
                            _, _ = await ucomm.add(cur, _, comm_data)
                        except Exception as exc:
                            logger.error("Rolling back update due to exception.")
                            logger.error(str(exc))
                            await conn.rollback()
                            raise
            await conn.commit()
    return data["rid"]


@_resolver.field("update_community")
async def update_community(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update community."""
    rid = await _update_community(
        parent,
        info,
        input,
    )

    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            community = await sql_community.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"community": community[0]}
