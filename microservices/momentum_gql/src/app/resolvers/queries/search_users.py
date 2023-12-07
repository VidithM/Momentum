"""Search users query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo
import aiohttp
import json

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    _info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search users."""
    search_terms = []
    if terms.get("rids"):
        str_rids = []
        for term in terms.get("rids"):
            str_rids.append(str(term))
        search_terms = search_terms + str_rids
    elif terms.get("emails"):
        search_terms = search_terms + terms.get("emails")
    query = {"terms": search_terms}
    print(query)
    async with aiohttp.ClientSession() as session:
        url = "http://host.docker.internal:8080/getuser"
        response = await session.get(url, json=query)
        print(response)
        data = await response.json(content_type="application/json")
        users = []
        if data != None:
            for user in data:
                user = json.loads(user)
                user["rid"] = int(user["rid"])
                users.append(user)
    return users


@_resolver.field("search_users")
async def search_users(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search users."""
    error: Optional[Dict[str, str]] = None

    users = await _search(
        parent,
        info,
        terms,
    )

    return {
        "users": users if users else None,
        "error": error,
    }
