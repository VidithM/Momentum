"""user mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _update_user(
    _: Any,
    info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a user."""
    if data.get("communities"):
        old_comm_list = []
        comm_list = data.get("communities")
        query = {"users": data["rid"]}
        async with aiohttp.ClientSession() as session:
            url = "http://localhost:8011/getcommunity"
            response = await session.get(url, json=query)
            data = await response.json(content_type="text/json")
        for item in data:
            if item["_id"] not in comm_list:
                async with aiohttp.ClientSession() as session:
                    updated_users = {"users": item["users"].remove(data["rid"])}
                    url = "http://localhost:8011/updatecommunity"
                    response = await session.post(url, json=updated_users)
                    data = await response.json(content_type="text/json")
            old_comm_list.append(item)
        for item in comm_list:
            if item not in old_comm_list:
                async with aiohttp.ClientSession() as session:
                    url = "http://localhost:8011/getcommunity"
                    response = await session.get(url, json=query)
                    data = await response.json(content_type="text/json")
                    data["users"].append(data["rid"])
                    url = "http://localhost:8011/updatecommunity"
                    response = await session.post(url, json=data)
                    data = await response.json(content_type="text/json")
        async with aiohttp.ClientSession() as session:
            url = "http://localhost:8080/updateuser"
            response = await session.post(url, json=data)
            resp = await response.json(content_type="text/json")
    return resp["rid"]


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

    query = {"rid": rid}
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8080/get"
        response = await session.get(url, json=query)
        data = await response.json(content_type="text/json")
    return {"user": data}
