# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# this file imports automatically (because it's __init__.py file)

from app.models.users_have_roles import users_have_roles  # noqa: F401
from app.models.request_logs import RequestLog  # noqa: F401

from app.models.conversions import Conversion  # noqa: F401

from app.models.label_categories import LabelCategory  # noqa: F401
from app.models.labels import Label  # noqa: F401
from app.models.recipes_have_labels import RecipeHasLabel  # noqa: F401
from app.models.oauth import OAuth  # noqa: F401

from app.models.users_have_event_roles import UserHasEventRole  # noqa: F401
