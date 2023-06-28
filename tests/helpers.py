from app.models.users import User
from flask_security import login_user


def with_authenticated_user(app, username):
    user = User.load_by_username(username)
    login_user(user)


def without_user(app):
    @app.login_manager.request_loader
    def no_user(request):
        return None


def playwright_login(page, username="user"):
    page.goto("login")

    # Interact with login form
    page.locator('input[name="email"]').fill(f"{username}@navarit.cz")
    page.locator('input[name="password"]').fill("navarit")
    page.locator('input[name="submit"]').click()
