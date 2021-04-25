from functools import wraps
from flask_security import current_user
from flask import abort


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and (
            current_user.is_admin or current_user.logged_from_admin
        ):
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorated_function
