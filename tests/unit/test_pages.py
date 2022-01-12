from tests.helpers import with_authenticated_user


def test_public_requests(app, client, db):
    # getting public page responses

    pages = [
        {"path": "/ingredients/show/1/", "code": 302},  # redirect to login
        {"path": "/recipes/show/1/", "code": 404},
        {"path": "/recipes/show/2/", "code": 200},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"


def test_requests_logged_in(app, db, client):
    with_authenticated_user(app, username="user")

    pages = [
        {"path": "/ingredients/show/1/", "code": 200},
        {"path": "/ingredients/show/2/", "code": 200},
        {"path": "/ingredients/show/3/", "code": 200},
        {"path": "/ingredients/show/4/", "code": 404},
        {"path": "/recipes/show/1/", "code": 200},
        {"path": "/recipes/pdf/1/", "code": 200},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"
