# from flask_dance.consumer.storage import MemoryStorage

# from app import google_oauth_bp


# GOOGLE OAUTH
# google login existing user with oauth
# should login

# google login existing user without oauth
# should create oauth and login

# google login noexisting user without oauth
# should create user (with invalid password hash), oauth, and login user


# def test_index_unauthorized(monkeypatch):
#     storage = MemoryStorage()
#     monkeypatch.setattr(google_oauth_bp, "storage", storage)

#     with app.test_client() as client:
#         response = client.get("/", base_url="https://example.com")

#     assert response.status_code == 302
#     assert response.headers["Location"] == "https://example.com/login/github"


# def test_index_authorized(monkeypatch):
#     storage = MemoryStorage({"access_token": "fake-token"})
#     monkeypatch.setattr(google_oauth_bp, "storage", storage)

#     with app.test_client() as client:
#         response = client.get("/")

#     assert response.status_code == 200
#     # text = response.get_data(as_text=True)
#     # assert text == "You are authorized"


# AUTH

# register
def test_register_valid(app, db, client):
    response = _register(client, "random@mail.com", "somepassword")
    assert b"V\xc3\xadtejte!" in response.data


# register - already existing user
def test_register_existing(app, db, client):
    response = _register(client, "admin@sk.cz", "someotherpassword")
    assert b"is already associated with an account." in response.data


# register - invalid email
def test_register_invalid(app, db, client):
    response = _register(client, "admin", "somepassword")
    print(response.data)
    assert b"Invalid email address" in response.data


# login user


def _register(client, email, password):
    return client.post(
        "/register",
        data=dict(email=email, password=password, password_confirm=password),
        follow_redirects=True,
    )


def _login(client, email, password):
    return client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )


def _logout(client):
    return client.get("/logout", follow_redirects=True)
