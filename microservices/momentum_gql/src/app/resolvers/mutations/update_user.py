"""user mutation resolver."""
import logging
from typing import Any, Dict, List

from ariadne import MutationType
from graphql import GraphQLResolveInfo
import aiohttp
import json

logger = logging.getLogger(__name__)

_resolver = MutationType()


async def _update_user(
    _: Any,
    _info: GraphQLResolveInfo,
    data: Dict[str, Any],
) -> List[Any]:
    """Update a user."""
    if data.get("communities") != None:
        old_comm_list = []
        comm_list = data.get("communities")
        query = {"users": data["rid"]}
        async with aiohttp.ClientSession() as session:
            url = "http://host.docker.internal:8011/getcommunity"
            response = await session.get(url, json=query)
            output = await response.json(content_type="application/json")
            print(output)
        for item in output["data"]:
            if item["rid"] not in comm_list:
                async with aiohttp.ClientSession() as session:
                    updated_users = {
                        "rid": item["rid"],
                        "users": item["users"].remove(data["rid"]),
                    }
                    print("Updated Users:")
                    print(updated_users)
                    if updated_users["users"] is None:
                        updated_users["users"] = []
                    url = "http://host.docker.internal:8011/updatecommunity"
                    response = await session.post(url, json=updated_users)
                    output = await response.json(content_type="text/json")
            old_comm_list.append(item["rid"])
        for item in comm_list:
            print(item)
            if item not in old_comm_list:
                async with aiohttp.ClientSession() as session:
                    query = {"rid": item}
                    url = "http://host.docker.internal:8011/getcommunity"
                    response = await session.get(url, json=query)
                    dictout = await response.json(content_type="application/json")
                    print(dictout)
                    if "users" not in dictout["data"][0].keys():
                        dictout["data"][0]["users"] = []
                    if dictout["data"][0]["users"] is None:
                        dictout["data"][0]["users"] = []
                    dictout["data"][0]["users"].append(data["rid"])
                    url = "http://host.docker.internal:8011/updatecommunity"
                    response = await session.post(url, json=dictout["data"][0])
                    output = await response.json(content_type="text/json")
    async with aiohttp.ClientSession() as session:
        data["rid"] = str(data["rid"])
        url = "http://host.docker.internal:8080/updateuser"
        response = await session.post(url, json=data)
        print(response)
    return str(data["rid"])


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

    query = {"terms": [rid]}
    async with aiohttp.ClientSession() as session:
        url = "http://host.docker.internal:8080/getuser"
        response = await session.get(url, json=query)
        user = await response.json(content_type="application/json")
        user = json.loads(user[0])
        user["rid"] = int(user["rid"])
    return {"user": user}
