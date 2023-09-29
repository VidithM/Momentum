"""Search comments query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...database import comments as sql_comments

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search comments."""
    return await sql_comments.search(info.context.db.cursor, info, terms)


@_resolver.field("search_comments")
async def search_comments(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search comments."""
    rids: Optional[List[int]] = None
    error: Optional[Dict[str, str]] = None

    rids = await _search(
        parent,
        info,
        terms,
    )

    return {
        "comments": sql_comments.search_by_rids(info.context.db.cursor, info, rids)
        if rids
        else None,
        "error": error,
    }
