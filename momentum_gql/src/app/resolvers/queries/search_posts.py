"""Search posts query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...database import posts as sql_posts

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search posts."""
    return await sql_posts.search(info.context.db.cursor, info, terms)


@_resolver.field("search_posts")
async def search_posts(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search posts."""
    rids: Optional[List[int]] = None
    error: Optional[Dict[str, str]] = None

    rids = await _search(
        parent,
        info,
        terms,
    )

    return {
        "posts": sql_posts.search_by_rids(info.context.db.cursor, info, rids)
        if rids
        else None,
        "error": error,
    }
