"""Add community mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import communities as sql_community
from ...database import user_community as ucomm

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_community(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a community."""
    async with info.context["db"].acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # await connection.begin()

            try:
                rid, _ = await sql_community.add(cur, parent, data)
            except Exception as exc:
                logger.error("Rolling back update due to exception.")
                logger.error(str(exc))
                await conn.rollback()
                raise
            # for user in data["users"]:
            #     comm_data = {}
            #     comm_data["user_id"] = user
            #     comm_data["community_id"] = rid
            #     try:
            #         _, _ = await ucomm.add(connection, parent, comm_data)
            #     except Exception as exc:
            #         logger.error("Rolling back update due to exception.")
            #         logger.error(str(exc))
            #         await info.context["db"].rollback()
            #         raise

            await conn.commit()

        return rid


@_resolver.field("create_community")
async def create_community(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve add community."""
    
    try:
        rid = await _add_community(
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
                print(rid)
                community = await sql_community.search_by_rids(cur, info, [rid])
                print(community)
    return {"community": community[0]}
