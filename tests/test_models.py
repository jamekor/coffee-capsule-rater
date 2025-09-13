from __future__ import annotations

from datetime import datetime

from app.models import Capsule, Rating, User


def test_rating_links_user_and_capsule() -> None:
    user = User(username="alice", email="alice@example.com", password="secret")
    capsule = Capsule(
        name="Espresso",
        brand="CoffeeCo",
        roast_level="medium",
        flavor_notes="chocolate",
    )
    rating = Rating(user=user, capsule=capsule, value=4, review="Nice")

    assert rating.user is user
    assert rating.capsule is capsule
    assert rating.value == 4
    assert isinstance(rating.timestamp, datetime)
