"""User SQL routines module."""
import logging
from typing import Any, Dict, List, Sequence, Tuple

import aiomysql

from . import util

logger = logging.getLogger(__name__)

TABLE = "communities"


async def _query(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Query database for community info."""
    logger.debug("* querying %s.%s %s", util.SCHEMA, TABLE, terms)

    base_query = f"""
        SELECT
            `main`.`id` AS `rid`,
            `main`.`description`,
            `main`.`users`,
        FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}

    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)
    await cursor.execute(query, args)
    rows = await cursor.fetchall()

    logger.debug("* query: %s.%s %s rows returned", util.SCHEMA, TABLE, len(rows))
    return rows


def _extract_setters(
    data: Dict[str, Any],
    args: Dict[str, Any],
    setters: List[str],
) -> None:
    """Extract info from the data object."""

    if data.get("description"):
        setters.append("`description` = %(description)s")
        args["description"] = data["description"]

    if data.get("users"):
        setters.append("`users` = %(users)s")
        args["users"] = data["users"]


def _extract_wheres(  # pylint: disable=too-many-branches, too-many-statements
    _,
    terms: Dict[str, Any],
    wheres: List[str],
    args: Dict[str, Any],
) -> None:
    """Extract info from the data object."""
    if terms.get("rids"):
        wheres.append("`id` IN %(rids)s")
        args["rids"] = terms["rids"]

    if terms.get("descriptions"):
        wheres.append("`description` IN %(descriptions)s")
        args["descriptions"] = terms["descriptions"]

    if terms.get("users"):
        wheres.append("`users` IN %(users)s")
        args["users"] = terms["users"]


async def add(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> Tuple[int, str]:
    """Add a community."""
    logger.debug("* insert: updating table %s.%s", util.SCHEMA, TABLE)

    query = f"""\
            INSERT INTO `{util.SCHEMA}`.`{TABLE}` SET
        """  # nosec

    args: Dict[str, Any] = {}
    setters: List[Any] = []

    _extract_setters(data, args, setters)

    query += "\n" + ",\n".join(setters)
    await cursor.execute(query, args)

    return cursor.lastrowid, args["rid"]


async def create_table(
    cursor: aiomysql.Cursor,
) -> bool:
    """Create the community table."""
    logger.debug("* creating table %s.%s", util.SCHEMA, TABLE)

    query = f"""
    CREATE TABLE IF NOT EXISTS `{util.SCHEMA}`.`{TABLE}` (
        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `description` text,
        `users` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
    );
    """
    try:
        await cursor.execute(query)
    except aiomysql.Error as err:
        logger.error("Could not create table %s.%s %s", util.SCHEMA, TABLE, err)
        raise

    return True


async def search_by_rids(
    cursor: aiomysql.Cursor,
    _,
    rids: Sequence[int],
) -> Dict[int, Any]:
    """Query database for community info."""
    terms = {
        "rids": rids,
    }
    return {row["rid"]: row for row in await _query(cursor, _, terms)}


async def search(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[int]:
    """Search Communities."""
    logger.debug("* search: querying table %s.%s", util.SCHEMA, TABLE)

    base_query = f"""\
            SELECT
                DISTINCT `id` as `rid`
            FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}
    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)

    await cursor.execute(query, args)

    rows = await cursor.fetchall()

    return [row[0] for row in rows]


async def update(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> None:
    """Update a community."""
    logger.debug("* update: updating table %s.%s", util.SCHEMA, TABLE)

    args: Dict[str, Any] = {}
    setters: List[str] = []
    wheres: List[str] = []

    query = f"""\
            UPDATE `{util.SCHEMA}`.`{TABLE}` SET
        """  # nosec
    wheres.append("`id` = %(rid)s")
    args["rid"] = data["rid"]

    _extract_setters(data, args, setters)

    if not setters:
        return

    query += "\n" + ",\n".join(setters)
    query += "\nWHERE " + " \nAND ".join(wheres)

    await cursor.execute(query, args)
