"""Search users query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo
import aiohttp

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    _info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search users."""
    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8080/search"
        response = await session.get(url, json=terms)
        data = await response.json(content_type="text/json")
    return data


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
