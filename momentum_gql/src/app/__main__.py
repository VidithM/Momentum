"""Main entry point for running from command line."""
import argparse
from typing import Any, Dict

import uvicorn

parser = argparse.ArgumentParser()

parser.add_argument(
    "--port",
    type=int,
    default=0,
    help="Port on which the server should listen.",
)

args = parser.parse_args()

uvicorn_args: Dict[str, Any] = {}

if args.port > 0:
    uvicorn_args["port"] = args.port

uvicorn.run(
    "app.main:create_app",
    host="0.0.0.0",                 # nosec (hardcoded_bind_all_interfaces)
    factory=True,
    **uvicorn_args
)
