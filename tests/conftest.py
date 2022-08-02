from tests.factories import IngredientFactory, RecipeFactory

import pytest

from app import create_app
from app import db as _db


@pytest.fixture
def app(scope="session"):
    application = create_app(config_name="testing")

    @application.context_processor
    def utility_processor():
        from app.helpers.context_processors import (
            human_format_date,
            link_to,
            link_to_edit,
            formatted_amount,
        )

        return dict(
            human_format_date=human_format_date,
            link_to=link_to,
            link_to_edit=link_to_edit,
            formatted_amount=formatted_amount,
        )

    return application


@pytest.fixture
def db(app):
    # insert default data
    with app.app_context():
        _db.create_all()

    db_fill()

    return _db


def db_fill():
    # from flask_security import create_user, create_role
    from app import security
    from app.models import Ingredient, Recipe

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
            username="user", email="user@sk.cz", password="pass123"
        ),
        security.datastore.create_user(
            username="application_manager",
            email="appmanager@sk.cz",
            roles=["application_manager"],
            password="pass123",
        ),
        security.datastore.create_user(
            username="admin", email="admin@sk.cz", roles=["admin"], password="pass123"
        ),
    ]

    for user in users:
        user.save()

    IngredientFactory(created_by=users[0].id).save(),
    IngredientFactory(created_by=users[0].id).save(),
    IngredientFactory(created_by=users[0].id).save(),

    recipe = RecipeFactory(portion_count=1)
    recipe.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe.save()

    recipe_2 = RecipeFactory(name="veřejný recept", shared=True)
    recipe_2.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe_2.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe_2.save()
