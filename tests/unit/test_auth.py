# GOOGLE OAUTH
# google login existing user with oauth
# should login

# google login existing user without oauth
# should create oauth and login

# google login noexisting user without oauth
# should create user (with invalid password hash), oauth, and login user

# AUTH

# register
def test_register_valid(app, db, client):
    response = _register(client, "random@mail.com", "somepassword")
    assert b"v\xc3\xadtejte!" in response.data


# register - already existing user
def test_register_existing(app, db, client):
    response = _register(client, "admin@sk.cz", "someotherpassword")
    assert b"is already associated with an account." in response.data


# register - invalid email
def test_register_invalid(app, db, client):
    response = _register(client, "admin", "somepassword")
    assert b"Invalid email address" in response.data


# login user
def test_login(app, db, client):
    response = _login(client, "admin@sk.cz", "pass123")
    assert b"v\xc3\xadtejte!" in response.data


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
