"""User SQL routines module."""
import logging
from typing import Any, Dict, List, Sequence, Tuple

import aiomysql

from . import util

logger = logging.getLogger(__name__)

TABLE = "users"


async def _query(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Query database for user info."""
    print("* querying %s.%s %s", util.SCHEMA, TABLE, terms)

    base_query = f"""
        SELECT
            `main`.`id` AS `rid`,
            `main`.`password`,
            `main`.`username`,
            `main`.`name`,
            `main`.`email`
        FROM `{util.SCHEMA}`.`{TABLE}` `main`
        """  # nosec

    wheres: List[str] = []
    args: Dict[str, Any] = {}

    _extract_wheres(_, terms, wheres, args)

    query = util.compose_query(base_query, wheres)
    await cursor.execute(query, args)
    rows = await cursor.fetchall()

    print("* query: %s.%s %s rows returned", util.SCHEMA, TABLE, len(rows))
    print(rows)
    return rows


def _extract_setters(
    data: Dict[str, Any],
    args: Dict[str, Any],
    setters: List[str],
) -> None:
    """Extract info from the data object."""

    if data.get("password"):
        setters.append("`password` = %(password)s")
        args["password"] = data["password"]

    if data.get("username"):
        setters.append("`username` = %(username)s")
        args["username"] = data["username"]

    if data.get("name"):
        setters.append("`name` = %(name)s")
        args["name"] = data["name"]

    if data.get("email"):
        setters.append("`email` = %(email)s")
        args["email"] = data["email"]


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

    if terms.get("usernames"):
        wheres.append("`username` IN %(usernames)s")
        args["usernames"] = terms["usernames"]

    if terms.get("names"):
        wheres.append("`name` IN %(names)s")
        args["names"] = terms["names"]

    if terms.get("emails"):
        wheres.append("`email` IN %(emails)s")
        args["emails"] = terms["emails"]


async def add(
    cursor: aiomysql.Cursor,
    _,
    data: Dict[str, Any],
) -> Tuple[int, str]:
    """Add a user."""
    print("* insert: updating table %s.%s", util.SCHEMA, TABLE)

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
    """Create the user table."""
    print("* creating table %s.%s", util.SCHEMA, TABLE)

    query = """
    CREATE TABLE IF NOT EXISTS `momentum`.`users` (
        `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `password` varchar(255) NOT NULL,
        `username` varchar(255) NOT NULL,
        `name` varchar(255) NOT NULL,
        `email` varchar(255) NOT NULL,
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
    print(terms)
    result = await _query(cursor, _, terms)
    print(result)
    return result


async def search(
    cursor: aiomysql.Cursor,
    _,
    terms: Dict[str, Any],
) -> List[int]:
    """Search Users."""
    print("* search: querying table %s.%s", util.SCHEMA, TABLE)

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
    """Update a user."""
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

    await cursor.execute(query, args)
