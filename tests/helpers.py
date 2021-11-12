from app.models.users import User


def with_authenticated_user(app, username=None):
    @app.login_manager.request_loader
    def load_user_from_request(request, username=username):
        user = User.query.first() if not username else User.load_by_username(username)
        if user is None:
            assert False
        else:
            return user
