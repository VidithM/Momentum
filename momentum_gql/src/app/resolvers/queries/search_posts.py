"""Search posts query resolver."""  # pylint: disable=invalid-name
import logging
from typing import Any, Dict, List, Optional

from ariadne import QueryType
from graphql import GraphQLResolveInfo
import aiomysql

from ...database import posts as sql_posts

logger = logging.getLogger(__name__)

_resolver = QueryType()


async def _search(
    _: Any,
    info: GraphQLResolveInfo,
    terms: Dict[str, Any],
) -> List[int]:
    """Search posts."""
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    return await sql_posts.search(cur, info, terms)


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
    print(rids)
    cur = await info.context["db"].cursor(aiomysql.DictCursor)
    posts = await sql_posts.search_by_rids(cur, info, rids)
    await cur.close()

    return {
        "posts": posts
        if rids
        else None,
        "error": error,
    }
