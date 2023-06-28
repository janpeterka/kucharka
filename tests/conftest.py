import pytest

from app import create_app
from app import db as _db

pytest_plugins = ["fixtures"]


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "storage_state": "tests/helpers/auth.json",
#         "ignore_https_errors": True,
#     }


@pytest.fixture(scope="session")
def app():
    application = create_app(config_name="test")

    @application.context_processor
    def utility_processor():
        from app.helpers.context_processors import context_processors
        from app.models import models_dictionary as models

        return dict(**context_processors, **models)

    return application


@pytest.fixture(scope="session")
def db(app):
    from sqlalchemy import text

    # insert default data
    with app.app_context():
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"):
            # sqlite is used in GitHub actions
            _db.create_all()
        else:
            _db.session.execute(text("drop database kucharka_test;"))
            _db.session.execute(text("create schema kucharka_test;"))
            _db.session.execute(text("use kucharka_test;"))
            _db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            _db.drop_all()
            _db.create_all()
            _db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    return _db


@pytest.fixture(autouse=True, scope="function")
def data(db):
    _clear_db(db)
    db_create_roles(db)
    db_create_default_data()
    # db_create_data(db)


def _clear_db(db):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def db_create_roles(_db):
    from app import security

    roles = [
        security.datastore.create_role(
            name="admin",
            permissions="manage-application,manage-users,login-as,see-debug,see-other,edit-other",
        ),
        security.datastore.create_role(
            name="application_manager",
            permissions="manage-application,see-other,edit-other",
        ),
    ]

    for role in roles:
        role.save()

    users = [
        security.datastore.create_user(
            id=1, username="user", email="user@navarit.cz", password="navarit"
        ),
        security.datastore.create_user(
            id=2,
            username="application_manager",
            email="appmanager@navarit.cz",
            roles=["application_manager"],
            password="navarit",
        ),
        security.datastore.create_user(
            id=3,
            username="admin",
            email="admin@navarit.cz",
            roles=["admin"],
            password="navarit",
        ),
    ]

    for user in users:
        user.save()


def db_create_default_data():
    from app.models import IngredientCategory, Measurement

    IngredientCategory(id=1, name="Maso a masné výrobky").save()
    IngredientCategory(id=2, name="Mléčné výrobky").save()
    IngredientCategory(id=3, name="Ovoce a zelenina").save()
    IngredientCategory(id=4, name="Suché").save()
    IngredientCategory(id=5, name="Koření").save()

    Measurement(id=1, name="gramy").save()
    Measurement(id=2, name="kusy").save()
