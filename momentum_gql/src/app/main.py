"""GraphQL app main module."""
import asyncio
import logging
import logging.config
import signal

import aiomysql
from ariadne.graphql import GraphQLSchema
from ariadne.types import ContextValue
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL


from dotenv import load_dotenv

from .resources.context import MyContext

from .resources.schema_utils import make_resolver_list

TIME_TO_QUIT = False


# pylint: disable=global-statement

logger = logging.getLogger(__name__)


async def update_context(loop) -> ContextValue:
    """Add extra information to the context."""

    return MyContext(
        db = await aiomysql.connect(host='127.0.0.1', port=3306,
                              user='root', password='rootpassword',
                              db='mysql', loop=loop),
    )


def load_schema() -> GraphQLSchema:
    """Load GraphQL schema."""
    logger.info("Loading schema")

    type_defs = load_schema_from_path("./src/app/resources/schema/")

    resolvers = make_resolver_list()


    logger.debug("Making executable schema")
    the_schema = make_executable_schema(
        type_defs,
        resolvers
    )
    logger.debug("Schema created")

    return the_schema

def _handle_quit_signals():
    """Handle signals that mean the program should exit."""
    global TIME_TO_QUIT
    TIME_TO_QUIT = True


def create_app():
    """Main loop"""
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, _handle_quit_signals)
    loop.add_signal_handler(signal.SIGTERM, _handle_quit_signals)
    update_context(loop)
    schema = load_schema()
    app = GraphQL(schema, debug=True)
    return app
