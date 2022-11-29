from tests.factories import IngredientFactory, RecipeFactory

import pytest

from app import create_app
from app import db as _db


@pytest.fixture(scope="session")
def app():
    application = create_app(config_name="testing")

    @application.context_processor
    def utility_processor():
        from app.helpers.context_processors import human_format_date, formatted_amount

        return dict(
            human_format_date=human_format_date,
            formatted_amount=formatted_amount,
        )

    return application


@pytest.fixture(scope="session")
def db(app):
    # insert default data
    with app.app_context():
        _db.drop_all()
        _db.create_all()

    return _db


@pytest.fixture(scope="function")
def data(db):
    _clear_db(db)
    db_set_roles()
    db_set_data()


def _clear_db(db):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


def db_set_roles():
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
            id=1, username="user", email="user@sk.cz", password="pass123"
        ),
        security.datastore.create_user(
            id=2,
            username="application_manager",
            email="appmanager@sk.cz",
            roles=["application_manager"],
            password="pass123",
        ),
        security.datastore.create_user(
            id=3,
            username="admin",
            email="admin@sk.cz",
            roles=["admin"],
            password="pass123",
        ),
    ]

    for user in users:
        user.save()


def db_set_data():
    # from flask_security import create_user, create_role
    from app.models import Ingredient, User

    IngredientFactory(created_by=User.load(1).id).save(),
    IngredientFactory(created_by=User.load(1).id).save(),
    IngredientFactory(created_by=User.load(1).id).save(),

    recipe = RecipeFactory(portion_count=1)
    recipe.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe.save()

    recipe_2 = RecipeFactory(name="veřejný recept", shared=True)
    recipe_2.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe_2.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe_2.save()
