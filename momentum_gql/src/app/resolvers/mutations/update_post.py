"""post mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql


from ...database import posts as sql_post

logger = logging.getLogger(__name__)

_resolver = MutationType()

async def _update_post(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a post."""
    async with info.context["db"].cursor(aiomysql.DictCursor) as connection:
        # await connection.begin()

        try:
            await sql_post.update(connection, info, data)
        except Exception:
            logger.error("Rolling back update due to exception.")
            await info.context["db"].rollback()
            raise


        await info.context["db"].commit()
    return data["rid"]


@_resolver.field("update_post")
async def update_post(
    parent,
    info: GraphQLResolveInfo,
    input: Dict[str, Any],  # pylint: disable=redefined-builtin
) -> Dict[str, Any]:
    """Resolve update post."""
    try:
        rid = await _update_post(
            parent,
            info,
            input,
        )
    except Exception as err:
        return {
            "error": str(err),
        }

    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    post = await sql_post.search_by_rids(cur, info, [rid])
    await cur.close()
    return {"post": post[0]}
