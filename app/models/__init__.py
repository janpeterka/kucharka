# This is needed for Flask-Migrate to work
# import all tables that are not classes (only raw M:N relationship tables)
# this file imports automatically (because it's __init__.py file)

from app.models.users_have_roles import users_have_roles