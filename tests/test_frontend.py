from pathlib import Path


def test_navigation_links_present():
    text = Path("frontend/index.html").read_text(encoding="utf-8")
    assert 'id="nav-capsules"' in text
    assert 'id="nav-add"' in text
    assert 'id="nav-profile"' in text
    assert 'id="nav-login"' in text
    assert 'id="nav-signup"' in text


def test_login_form_fields():
    text = Path("frontend/index.html").read_text(encoding="utf-8")
    assert 'id="login-form"' in text
    assert 'name="username"' in text
    assert 'name="password"' in text
