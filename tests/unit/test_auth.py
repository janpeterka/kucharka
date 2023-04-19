# GOOGLE OAUTH
# google login existing user with oauth
# should login

# google login existing user without oauth
# should create oauth and login

# google login noexisting user without oauth
# should create user (with invalid password hash), oauth, and login user

# AUTH


# login user
def test_login(app, db, client):
    response = _login(client, "admin@sk.cz", "pass123")
    assert b"v\xc3\xadtej!" in response.data


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
