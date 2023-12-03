"""community mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp


logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _update_community(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a community."""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/updatecommunity"
        response = await session.post(url, json=data)
        data = await response.json(content_type="text/json")
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
    query = {"rid": rid}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"community": data[0]}
