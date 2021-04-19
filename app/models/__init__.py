# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# this file imports automatically (because it's __init__.py file)

from app.models.users_have_roles import users_have_roles  # noqa: F401


# This is needed for ExtendedFlaskView to automatically import all Model classes
from .ingredients import Ingredient  # noqa: F401
from .recipes import Recipe  # noqa: F401
from .users import User  # noqa: F401
