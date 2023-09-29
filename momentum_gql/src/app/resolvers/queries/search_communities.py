"""Search communities query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...database import communities as sql_communities

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search communities."""
    return await sql_communities.search(info.context.db.cursor, info, terms)


@_resolver.field("search_communities")
async def search_communities(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search communities."""
    rids: Optional[List[int]] = None
    error: Optional[Dict[str, str]] = None

    rids = await _search(
        parent,
        info,
        terms,
    )

    return {
        "communities": sql_communities.search_by_rids(info.context.db.cursor, info, rids)
        if rids
        else None,
        "error": error,
    }
