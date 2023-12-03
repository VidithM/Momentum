"""Search communities query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo
import aiomysql
import aiohttp

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[Any]:
    """Search communities."""

    async with aiohttp.ClientSession() as session:
        url = "http://localhost:8005/getcommunity"
        response = await session.get(url, json=terms)
        data = await response.json(content_type="text/json")
    return data


@_resolver.field("search_communities")
async def search_communities(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search communities."""
    error: Optional[Dict[str, str]] = None

    communities = await _search(
        parent,
        info,
        terms,
    )

    return {"communities": communities if communities else None, "error": error}
