"""Minimal HTTP server for coffee capsule rater."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, List, Tuple
from urllib.parse import urlparse

from .models import Capsule, Rating, User


logger = logging.getLogger(__name__)


class AppHandler(BaseHTTPRequestHandler):
    """Very small REST API for users, capsules and ratings."""

    users: Dict[int, User] = {}
    capsules: Dict[int, Capsule] = {}
    ratings: Dict[int, List[Rating]] = {}
    next_user_id: int = 1
    next_capsule_id: int = 1

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    @classmethod
    def reset(cls) -> None:
        cls.users = {}
        cls.capsules = {}
        cls.ratings = {}
        cls.next_user_id = 1
        cls.next_capsule_id = 1

    def _send_json(self, data: object, status: int = 200) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _parse_json(self) -> Dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def _auth_user(self) -> User | None:
        header = self.headers.get("X-User-ID")
        if not header:
            return None
        try:
            user_id = int(header)
        except ValueError:
            return None
        return self.users.get(user_id)

    # ------------------------------------------------------------------
    # logging
    # ------------------------------------------------------------------
    def log_message(self, format: str, *args) -> None:  # noqa: D401, N802
        """Redirect standard log messages to the module logger."""

        logger.info("%s - - %s", self.address_string(), format % args)

    # ------------------------------------------------------------------
    # request handlers
    # ------------------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802 - required name
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if not parts:
            self._send_json({"message": "Coffee capsule rater is running!"})
            return

        if parts[0] == "capsules":
            if len(parts) == 1:
                data = [self._capsule_dict(c) for c in self.capsules.values()]
                self._send_json(data)
                return
            try:
                capsule_id = int(parts[1])
            except ValueError:
                self.send_error(404)
                return
            capsule = self.capsules.get(capsule_id)
            if not capsule:
                self.send_error(404)
                return
            if len(parts) == 2:
                self._send_json(self._capsule_dict(capsule))
                return
            if len(parts) == 3 and parts[2] == "ratings":
                ratings = [
                    self._rating_dict(r) for r in self.ratings.get(capsule_id, [])
                ]
                self._send_json(ratings)
                return

        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802 - required name
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if parts == ["users"]:
            data = self._parse_json()
            try:
                username = str(data["username"])
                email = str(data["email"])
                password = str(data["password"])
            except KeyError:
                self.send_error(400, "Missing fields")
                return
            user_id = self.next_user_id
            self.next_user_id += 1
            hashed = sha256(password.encode()).hexdigest()
            user = User(username=username, email=email, password=hashed, id=user_id)
            self.users[user_id] = user
            self._send_json({"id": user_id, "username": username, "email": email}, 201)
            return

        if parts == ["login"]:
            data = self._parse_json()
            try:
                username = str(data["username"])
                password = str(data["password"])
            except KeyError:
                self.send_error(400, "Missing fields")
                return
            user = next(
                (u for u in self.users.values() if u.username == username), None
            )
            if not user:
                self.send_error(401)
                return
            hashed = sha256(password.encode()).hexdigest()
            if hashed != user.password:
                self.send_error(401)
                return
            self._send_json(
                {
                    "token": user.id,
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            )
            return

        if parts == ["capsules"]:
            user = self._auth_user()
            if not user:
                self.send_error(401)
                return
            data = self._parse_json()
            try:
                name = str(data["name"])
                brand = str(data["brand"])
                roast = str(data["roast_level"])
                flavor = str(data.get("flavor_notes", ""))
            except KeyError:
                self.send_error(400, "Missing fields")
                return
            cid = self.next_capsule_id
            self.next_capsule_id += 1
            capsule = Capsule(
                name=name, brand=brand, roast_level=roast, flavor_notes=flavor, id=cid
            )
            self.capsules[cid] = capsule
            self._send_json(self._capsule_dict(capsule), 201)
            return

        if len(parts) == 3 and parts[0] == "capsules" and parts[2] == "ratings":
            user = self._auth_user()
            if not user:
                self.send_error(401)
                return
            try:
                capsule_id = int(parts[1])
            except ValueError:
                self.send_error(404)
                return
            capsule = self.capsules.get(capsule_id)
            if not capsule:
                self.send_error(404)
                return
            data = self._parse_json()
            try:
                value = int(data["value"])
            except KeyError:
                self.send_error(400, "Missing value")
                return
            if not 1 <= value <= 5:
                self.send_error(400, "Invalid rating")
                return
            review = str(data.get("review", ""))
            rating = Rating(
                user=user,
                capsule=capsule,
                value=value,
                review=review,
                timestamp=datetime.utcnow(),
            )
            self.ratings.setdefault(capsule_id, []).append(rating)
            self._send_json(self._rating_dict(rating), 201)
            return

        self.send_error(404)

    def do_PUT(self) -> None:  # noqa: N802 - required name
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if len(parts) == 2 and parts[0] == "users":
            user = self._auth_user()
            if not user:
                self.send_error(401)
                return
            try:
                uid = int(parts[1])
            except ValueError:
                self.send_error(404)
                return
            if user.id != uid:
                self.send_error(403)
                return
            data = self._parse_json()
            username = data.get("username")
            email = data.get("email")
            if username:
                user.username = str(username)
            if email:
                user.email = str(email)
            self._send_json(
                {"id": user.id, "username": user.username, "email": user.email}
            )
            return

        self.send_error(404)

    # ------------------------------------------------------------------
    # serializers
    # ------------------------------------------------------------------
    def _capsule_dict(self, capsule: Capsule) -> Dict[str, object]:
        ratings = self.ratings.get(capsule.id, [])
        avg = sum(r.value for r in ratings) / len(ratings) if ratings else None
        return {
            "id": capsule.id,
            "name": capsule.name,
            "brand": capsule.brand,
            "roast_level": capsule.roast_level,
            "flavor_notes": capsule.flavor_notes,
            "average_rating": avg,
        }

    def _rating_dict(self, rating: Rating) -> Dict[str, object]:
        return {
            "user_id": rating.user.id,
            "value": rating.value,
            "review": rating.review,
            "timestamp": rating.timestamp.isoformat(),
        }


def create_server(address: Tuple[str, int] = ("127.0.0.1", 0)) -> ThreadingHTTPServer:
    """Create a server bound to *address* for use in tests or scripts."""

    AppHandler.reset()
    return ThreadingHTTPServer(address, AppHandler)


def run() -> None:
    """Run a server using environment configuration.

    ``HOST`` defines the bind address (defaults to ``0.0.0.0``) and ``PORT``
    defines the port (defaults to ``8000``).  If ``LOG_FILE`` is set, all log
    output is additionally written to that file.
    """

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_file = os.getenv("LOG_FILE")

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
    )

    server = create_server((host, port))
    try:
        logger.info("Starting server on %s:%s", host, port)
        server.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - manual shutdown
        logger.info("Shutdown requested")
    finally:
        server.server_close()


if __name__ == "__main__":  # pragma: no cover - manual execution
    run()
