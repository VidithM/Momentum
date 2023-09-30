"""Add community mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import communities as sql_community

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_community(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a community."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            rid, _ = await sql_community.add(connection, parent, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise

        await info.context["db"].commit()

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

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    community = await sql_community.search_by_rids(cur, info, [rid])
    print(community)
    cur.close()
    return {"community": community[0]}
