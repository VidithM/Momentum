"""Search users query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ...database import users as sql_users

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search users."""
    return await sql_users.search(info.context.db.cursor, info, terms)


@_resolver.field("search_users")
async def search_users(
    parent,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> Dict[str, Any]:
    """Resolve search users."""
    rids: Optional[List[int]] = None
    error: Optional[Dict[str, str]] = None

    rids = await _search(
        parent,
        info,
        terms,
    )

    return {
        "users": sql_users.search_by_rids(info.context.db.cursor, info, rids)
        if rids
        else None,
        "error": error,
    }
