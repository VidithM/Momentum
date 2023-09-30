"""Request context module."""

from dataclasses import dataclass

import aiomysql


@dataclass
class MyContext:
    """A request context class."""

    db: aiomysql.Connection
