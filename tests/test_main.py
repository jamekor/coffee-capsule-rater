from __future__ import annotations

import json
from threading import Thread
from urllib.request import urlopen

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import create_server


def test_read_root() -> None:
    server = create_server()
    host, port = server.server_address
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        with urlopen(f"http://{host}:{port}/") as resp:
            assert resp.status == 200
            data = json.load(resp)
        assert data == {"message": "Coffee capsule rater is running!"}
    finally:
        server.shutdown()
        thread.join()
