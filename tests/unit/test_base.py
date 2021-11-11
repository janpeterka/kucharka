from tests.helpers import with_authenticated_user


def test_application(app):
    # testing app is correctly set

    # from conftest < .env.test
    assert app.config["WTF_CSRF_ENABLED"] is False
    # from config.py
    assert app.config["TESTING"] is True


def test_public_requests(app, client, db):
    # getting public page responses
    pages = [
        {"path": "/login", "code": 200},
        {"path": "/register", "code": 200},
        {"path": "/public-recipes/public-index/", "code": 200},
        {"path": "recepty", "code": 308},
        {"path": "/dashboard/", "code": 302},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"


def test_requests_logged_in(app, db, client):

    with_authenticated_user(app)

    pages = [
        {"path": "/dashboard", "code": 308, "redirect_path": "/dashboard/"},
        {"path": "/dashboard/", "code": 200},
        {"path": "/recipes/", "code": 200},
        {"path": "/ingredients/", "code": 200},
        {"path": "/public-recipes/", "code": 200},
        {"path": "/events/", "code": 200},
        {
            "path": "/public-recipes/public-index/",
            "code": 302,
            "redirect_path": "/public-recipes/",
        },
        {"path": "/login", "code": 302, "redirect_path": "/dashboard/"},
        {"path": "/", "code": 302, "redirect_path": "/dashboard/"},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"
