from app.models.users import User
from app import security


def create_user(username="test", password="testtest"):
    valid_user = {
        "username": f"{username}",
        "email": "test_user@test.com",
        "password": f"{password}",
    }
    # from flask import current_app

    user = security.datastore.create_user(**valid_user)
    security.datastore.activate_user(user)

    return user


def with_authenticated_user(app, username=None):
    @app.login_manager.request_loader
    def load_user_from_request(request, username=username):
        user = User.query.first() if not username else User.load_by_username(username)
        if user is None:
            assert False
        else:
            return user


def _get_password_hash(password):
    import bcrypt

    if not isinstance(password, bytes) and password is not None:
        password = password.encode("utf-8")

    return bcrypt.hashpw(password, bcrypt.gensalt())
