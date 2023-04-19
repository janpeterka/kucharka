from app.models.users import User


def with_authenticated_user(app, username):
    @app.login_manager.request_loader
    def load_user_from_request(request, username=username):
        user = User.load_by_username(username)
        if user is None:
            assert False
        else:
            return user


def without_user(app):
    @app.login_manager.request_loader
    def no_user(request):
        return None


def playwright_login(page, username="user"):
    page.goto("login")

    # Interact with login form
    page.locator('input[name="email"]').fill(f"{username}@skautskakucharka.cz")
    page.locator('input[name="password"]').fill("navarit")
    page.locator('input[name="submit"]').click()
