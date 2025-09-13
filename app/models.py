from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Simple representation of an application user."""

    username: str
    email: str
    password: str
    id: int | None = None


@dataclass
class Capsule:
    """Data about a coffee capsule entry."""

    name: str
    brand: str
    roast_level: str
    flavor_notes: str = ""
    id: int | None = None


@dataclass
class Rating:
    """User-provided rating for a given capsule."""

    user: User
    capsule: Capsule
    value: int
    review: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
