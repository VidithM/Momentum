"""User SQL routines module."""
import logging
from typing import Any, Dict, List, Sequence, Tuple

import aiomysql

from . import util

logger = logging.getLogger(__name__)

TABLE = "user_community"


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
            `main`.`user_id`,
            `main`.`community_id`
        FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}

    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)
    await cursor.execute(query, args)
    rows = list(await cursor.fetchall())

    logger.debug("* query: %s.%s %s rows returned", util.SCHEMA, TABLE, len(rows))
    return rows


def _extract_setters(
    data: Dict[str, Any],
    args: Dict[str, Any],
    setters: List[str],
) -> None:
    """Extract info from the data object."""
    print(data)
    if data.get("user_id") != None:
        setters.append("`user_id` = %(user_id)s")
        args["user_id"] = data["user_id"]

    if data.get("community_id") != None:
        setters.append("`community_id` = %(community_id)s")
        args["community_id"] = data["community_id"]
    print(setters)


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

    if terms.get("user_ids"):
        wheres.append("`user_id` IN %(user_ids)s")
        args["user_ids"] = terms["user_ids"]

    if terms.get("community_ids"):
        wheres.append("`community_id` IN %(community_ids)s")
        args["community_ids"] = terms["community_ids"]


async def add(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> Tuple[int, str]:
    """Add a record."""
    logger.debug("* insert: updating table %s.%s", util.SCHEMA, TABLE)

    query = f"""\
            INSERT INTO `{util.SCHEMA}`.`{TABLE}` SET
        """  # nosec

    args: Dict[str, Any] = {}
    setters: List[Any] = []

    _extract_setters(data, args, setters)

    query += "\n" + ",\n".join(setters)
    await cursor.execute(query, args)

    return cursor.lastrowid, args.get("rid", "")


async def create_table(
    cursor: aiomysql.Cursor,
) -> bool:
    """Create the user_community table."""
    logger.debug("* creating table %s.%s", util.SCHEMA, TABLE)

    query = """
    CREATE TABLE IF NOT EXISTS `momentum`.`user_community` (
        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `user_id` int(10),
        `community_id`int(10),
        PRIMARY KEY (`id`)
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
) -> List[Dict[str, Any]]:
    """Query database for record info."""
    terms = {
        "rids": rids,
    }
    return await _query(cursor, _, terms)


async def search_by_user_ids(
    cursor: aiomysql.Cursor,
    _,
    rids: Sequence[int],
) -> List[int]:
    """Search Communities."""
    logger.debug("* search: querying table %s.%s", util.SCHEMA, TABLE)
    if rids == []:
        return []
    terms = {
        "user_ids": rids,
    }
    base_query = f"""\
            SELECT
                `community_id` as `rid`
            FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}
    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)

    await cursor.execute(query, args)
    rows = await cursor.fetchall()
    return [row["rid"] for row in rows]


async def search_by_community_ids(
    cursor: aiomysql.Cursor,
    _,
    rids: Sequence[int],
) -> List[int]:
    """Search Communities."""
    logger.debug("* search: querying table %s.%s", util.SCHEMA, TABLE)
    if rids == []:
        return []
    terms = {
        "community_ids": rids,
    }
    base_query = f"""\
            SELECT
                DISTINCT `user_id` as `rid`
            FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}
    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)

    await cursor.execute(query, args)
    rows = await cursor.fetchall()
    return [row["rid"] for row in rows]


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
    print(rows)
    return [row["rid"] for row in rows]


async def update(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> None:
    """Update a community."""
    print("* update: updating table %s.%s", util.SCHEMA, TABLE)
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
    print(cursor.mogrify(query))
    print(args)
    await cursor.execute(query, args)
