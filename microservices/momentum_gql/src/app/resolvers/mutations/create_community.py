"""Add community mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp


logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_community(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a community."""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/newcommunity"
        response = await session.post(url, json=data)
        data = await response.json(content_type="text/json")
    return data["rid"]


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
    query = {"rid": rid}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"community": data[0]}
