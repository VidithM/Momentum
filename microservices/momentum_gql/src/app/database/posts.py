"""User SQL routines module."""
import logging
from typing import Any, Dict, List, Sequence, Tuple

import aiomysql

from . import util

logger = logging.getLogger(__name__)

TABLE = "posts"


async def _query(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Query database for post info."""
    logger.debug("* querying %s.%s %s", util.SCHEMA, TABLE, terms)

    base_query = f"""
        SELECT
            `main`.`id` AS `rid`,
            `main`.`user`,
            `main`.`content`,
            `main`.`community`,
            `main`.`timestamp`,
            `main`.`file`
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

    if data.get("user"):
        setters.append("`user` = %(user)s")
        args["user"] = data["user"]

    if data.get("content"):
        setters.append("`content` = %(content)s")
        args["content"] = data["content"]

    if data.get("community"):
        setters.append("`community` = %(community)s")
        args["community"] = data["community"]

    if data.get("timestamp"):
        setters.append("`timestamp` = %(timestamp)s")
        args["timestamp"] = data["timestamp"]

    if data.get("file"):
        setters.append("`file` = %(file)s")
        args["file"] = data["file"]


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

    if terms.get("users"):
        wheres.append("`user` IN %(users)s")
        args["users"] = terms["users"]

    if terms.get("contents"):
        wheres.append("`content` IN %(contents)s")
        args["contents"] = terms["contents"]

    if terms.get("communities"):
        wheres.append("`community` IN %(communities)s")
        args["communities"] = terms["communities"]

    if terms.get("timestamp"):
        wheres.append("`main`.`timestamp` <= %(timestamp_end)s")
        args["timestamp_end"] = terms["timestamp"]["end_time"]

        wheres.append("`main`.`timestamp` >= %(timestamp_start)s")
        args["timestamp_start"] = terms["timestamp"]["start_time"]


async def add(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> Tuple[int, str]:
    """Add a post."""
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
    """Create the post table."""
    logger.debug("* creating table %s.%s", util.SCHEMA, TABLE)

    query = """
    CREATE TABLE IF NOT EXISTS `momentum`.`posts` (
        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `user` varchar(255) NOT NULL,
        `content` text NOT NULL,
        `community` int(10) NOT NULL,
        `timestamp` DATETIME NOT NULL,
        `file` MEDIUMBLOB,
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
    """Query database for user info."""
    terms = {
        "rids": rids,
    }
    return await _query(cursor, _, terms)


async def search(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[int]:
    """Search Users."""
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

    return [row["rid"] for row in rows]


async def update(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> None:
    """Update a post."""
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
