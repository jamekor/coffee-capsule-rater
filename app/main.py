"""Minimal HTTP server for coffee capsule rater."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Tuple


class CapsuleHandler(BaseHTTPRequestHandler):
    """Request handler serving a single health-check endpoint."""

    def do_GET(
        self,
    ) -> None:  # noqa: N802  (method name required by BaseHTTPRequestHandler)
        if self.path != "/":
            self.send_error(404)
            return

        body = json.dumps({"message": "Coffee capsule rater is running!"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(address: Tuple[str, int] = ("127.0.0.1", 0)) -> ThreadingHTTPServer:
    """Create a server bound to *address* for use in tests or scripts."""

    return ThreadingHTTPServer(address, CapsuleHandler)


def run() -> None:
    """Run a development server on port 8000."""

    server = create_server(("127.0.0.1", 8000))
    try:
        server.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - manual shutdown
        pass
    finally:
        server.server_close()


if __name__ == "__main__":  # pragma: no cover - manual execution
    run()
