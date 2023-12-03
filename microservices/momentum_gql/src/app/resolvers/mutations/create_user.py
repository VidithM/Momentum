"""Add user mutation resolver."""
import logging
from typing import Any, Dict

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _add_user(
    parent: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> int:
    """Create a user."""
    async with aiohttp.ClientSession() as session:
        url = "redisurl"
        response = await session.post(url, json=data)
        data = await response.json(content_type="text/json")
    return data["rid"]


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
    query = {"rid": rid}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"community": data[0]}
