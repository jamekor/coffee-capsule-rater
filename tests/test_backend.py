from __future__ import annotations

import json
from threading import Thread
from urllib.request import Request, urlopen

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import create_server


def _request(method: str, url: str, data: dict | None = None, headers: dict | None = None):
    if data is not None:
        body = json.dumps(data).encode()
        headers = {"Content-Type": "application/json", **(headers or {})}
    else:
        body = None
        headers = headers or {}
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req) as resp:
        return resp.status, json.load(resp)


def test_full_backend_flow() -> None:
    server = create_server()
    host, port = server.server_address
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    base = f"http://{host}:{port}"
    try:
        # register user
        status, user = _request(
            "POST",
            f"{base}/users",
            {"username": "alice", "email": "alice@example.com", "password": "secret"},
        )
        assert status == 201
        user_id = user["id"]

        # login
        status, login = _request(
            "POST",
            f"{base}/login",
            {"username": "alice", "password": "secret"},
        )
        assert status == 200
        token = login["token"]

        # edit profile
        status, updated = _request(
            "PUT",
            f"{base}/users/{user_id}",
            {"email": "new@example.com"},
            {"X-User-ID": str(token)},
        )
        assert status == 200
        assert updated["email"] == "new@example.com"

        # create capsule
        status, capsule = _request(
            "POST",
            f"{base}/capsules",
            {"name": "Espresso", "brand": "CoffeeCo", "roast_level": "medium"},
            {"X-User-ID": str(token)},
        )
        assert status == 201
        capsule_id = capsule["id"]

        # list capsules
        status, capsules = _request("GET", f"{base}/capsules")
        assert status == 200
        assert len(capsules) == 1
        assert capsules[0]["id"] == capsule_id

        # submit rating
        status, rating = _request(
            "POST",
            f"{base}/capsules/{capsule_id}/ratings",
            {"value": 5, "review": "Great"},
            {"X-User-ID": str(token)},
        )
        assert status == 201
        assert rating["value"] == 5

        # list ratings
        status, ratings = _request("GET", f"{base}/capsules/{capsule_id}/ratings")
        assert status == 200
        assert len(ratings) == 1
        assert ratings[0]["value"] == 5

        # retrieve capsule with average rating
        status, capsule_detail = _request("GET", f"{base}/capsules/{capsule_id}")
        assert status == 200
        assert capsule_detail["average_rating"] == 5.0
    finally:
        server.shutdown()
        thread.join()

