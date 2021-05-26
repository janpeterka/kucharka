from functools import wraps
from flask_security import current_user
from flask import abort


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_role("superadmin"):
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorated_function


def app_manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_role("app manager"):
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorated_function


def app_manager_or_higher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and (
            current_user.has_role("app manager")
            or current_user.has_role("admin")
            or current_user.has_role("superadmin")
        ):
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorated_function
