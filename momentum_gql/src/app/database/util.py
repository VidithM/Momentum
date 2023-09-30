"""Util database module."""
import logging
from typing import List, Optional


logger = logging.getLogger(__name__)

SCHEMA = "momentum"


def compose_query(
    base_query: str,
    wheres: List[str],
    more_wheres: Optional[List[str]] = None,
    joins: Optional[List[str]] = None,
    order_bys: Optional[List[str]] = None,
) -> str:
    """Compose the full query from parts."""
    joins_str = "\n".join(joins) if joins else ""
    wheres_str = ""
    order_bys_str = ""

    all_wheres = wheres + more_wheres if more_wheres is not None else wheres

    if all_wheres:
        wheres_str += """ WHERE """ + all_wheres.pop()

    if all_wheres:
        wheres_str += """ \nAND """ + " \nAND ".join(all_wheres)

    if order_bys:
        order_bys_str = """ ORDER BY """ + ",".join(order_bys)

    return f"""
        {base_query}
        {joins_str}
        {wheres_str}
        {order_bys_str}
    """
