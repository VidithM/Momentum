"Main module"
import json
import http.server
import socketserver
from typing import Tuple
from http import HTTPStatus
from dotenv import dotenv_values
from pymongo import MongoClient

from .database.communities import (
    update_community,
    create_new_community,
    delete_community,
    query_community,
)

config = dotenv_values(".env")


class Handler(http.server.SimpleHTTPRequestHandler):
    "HTTP handler class"

    def __init__(
        self,
        request: bytes,
        client_address: Tuple[str, int],
        server: socketserver.BaseServer,
    ):
        super().__init__(request, client_address, server)

    def do_GET(self):
        "Handle GET requests"
        print(self.path)
        if self.path == "/getcommunity":
            content_length = int(self.headers["Content-Length"])
            if content_length:
                input_json = self.rfile.read(content_length)
                input_data = json.loads(input_json)
            else:
                input_data = None
            mongodb_client = MongoClient(config["ME_CONFIG_MONGODB_URL"])
            database = mongodb_client[config["DB_NAME"]]
            mycol = database["customers"]
            community = query_community(mycol, input_data)

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            output_data = {
                "status": "OK",
                "message": "Get community!",
                "data": community,
            }
            output_json = json.dumps(output_data, default=str)
            self.wfile.write(output_json.encode("utf-8"))
        elif self.path == "/":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            output_data = {"status": "OK", "message": "Working!"}
            output_json = json.dumps(output_data)
            self.wfile.write(output_json.encode("utf-8"))
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            output_data = {"status": "NOT FOUND", "message": "Endpoint Not Found"}
            output_json = json.dumps(output_data)
            self.wfile.write(output_json.encode("utf-8"))

    def do_POST(self):  # pylint: disable=C0103
        "Handle POST requests"
        # - request -
        print(self.path)
        if self.path == "/newcommunity":
            content_length = int(self.headers["Content-Length"])

            if content_length:
                input_json = self.rfile.read(content_length)
                input_data = json.loads(input_json)
            else:
                input_data = None

            mongodb_client = MongoClient(config["ME_CONFIG_MONGODB_URL"])
            database = mongodb_client[config["DB_NAME"]]
            mycol = database["customers"]
            rid = create_new_community(mycol, input_data)

            # - response -

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/json")
            self.end_headers()

            output_data = {"status": "OK", "data": rid}
            output_json = json.dumps(output_data)

            self.wfile.write(output_json.encode("utf-8"))
        elif self.path == "/updatecommunity":
            content_length = int(self.headers["Content-Length"])
            if content_length:
                input_json = self.rfile.read(content_length)
                input_data = json.loads(input_json)
            else:
                input_data = None

            mongodb_client = MongoClient(config["ME_CONFIG_MONGODB_URL"])
            database = mongodb_client[config["DB_NAME"]]
            mycol = database["customers"]
            rid = update_community(mycol, input_data)

            # - response -

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/json")
            self.end_headers()

            output_data = {"status": "OK", "data": rid}
            output_json = json.dumps(output_data)

            self.wfile.write(output_json.encode("utf-8"))
        elif self.path == "/deletecommunity":
            content_length = int(self.headers["Content-Length"])
            if content_length:
                input_json = self.rfile.read(content_length)
                input_data = json.loads(input_json)
            else:
                input_data = None

            mongodb_client = MongoClient(config["ME_CONFIG_MONGODB_URL"])
            database = mongodb_client[config["DB_NAME"]]
            mycol = database["customers"]
            delete_community(mycol, input_data)

            # - response -

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/json")
            self.end_headers()

            output_data = {"status": "OK"}
            output_json = json.dumps(output_data)

            self.wfile.write(output_json.encode("utf-8"))
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                bytes(json.dumps({"message": "Endpoint not found"}).encode())
            )


def main():
    "Main"
    PORT = 8005
    # Create an object of the above class
    my_server = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
    # Star the server
    print(f"Server started at {PORT}")
    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping by Ctrl+C")
        my_server.server_close()


if __name__ == "__main__":
    main()
