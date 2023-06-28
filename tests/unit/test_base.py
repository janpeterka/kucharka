import pytest
from tests.helpers import with_authenticated_user


@pytest.fixture
def ingredients(app, db):
    from tests.factories import IngredientFactory

    IngredientFactory().save()


def test_application(app):
    # testing app is correctly set

    # from conftest < .env.test
    assert app.config["WTF_CSRF_ENABLED"] is False
    # from config.py
    assert app.config["TESTING"] is True


def test_public_requests(app, client):
    # getting public page responses
    pages = [
        {"path": "/login", "code": 200},
        {"path": "/register", "code": 200},
        {"path": "/public-recipe/public", "code": 200},
        {"path": "/recepty", "code": 302},
        {"path": "/dashboard/", "code": 302},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"


def test_requests_logged_in(app, ingredients, client):
    with_authenticated_user(app, username="user")

    pages = [
        {"path": "/dashboard", "code": 308, "redirect_path": "/dashboard/"},
        {"path": "/dashboard/", "code": 200},
        {"path": "/recipe/", "code": 200},
        {"path": "/ingredient/", "code": 200},
        {"path": "/public-recipe/", "code": 200},
        {"path": "/event/", "code": 200},
        {
            "path": "/public-recipe/public",
            "code": 302,
            "redirect_path": "/public-recipe/",
        },
        {"path": "/login", "code": 302, "redirect_path": "/dashboard/"},
        {"path": "/", "code": 302, "redirect_path": "/dashboard/"},
        {"path": "/measurement/", "code": 404},
        {"path": "/file/", "code": 404},
    ]

    for page in pages:
        response = client.get(page["path"])
        assert response == page["code"], f"path: {page['path']}"


def test_requests_admin_logged_in(app, db, client):
    with_authenticated_user(app, username="admin")

    pages = [
        {"path": "/measurement/", "code": 200},
        {"path": "/file/", "code": 200},
    ]

    for page in pages:
        response = client.get(page["path"])
        assert response == page["code"], f"path: {page['path']}"


def test_requests_app_manager_logged_in(app, db, client):
    with_authenticated_user(app, username="application_manager")

    pages = [
        {"path": "/measurement/", "code": 200},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"
