import pytest
from tests.helpers import with_authenticated_user, without_user


@pytest.fixture
def recipes(db):
    from app.models import Ingredient, User
    from tests.factories import IngredientFactory, RecipeFactory

    IngredientFactory(id=1, created_by=User.load(1).id).save(),
    IngredientFactory(id=2, created_by=User.load(1).id).save(),
    IngredientFactory(id=3, created_by=User.load(1).id).save(),

    recipe = RecipeFactory(id=1, portion_count=1)
    recipe.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe.save()

    recipe_2 = RecipeFactory(id=2, name="veřejný recept", shared=True)
    recipe_2.add_ingredient(Ingredient.load_all()[0], amount=20)
    recipe_2.add_ingredient(Ingredient.load_all()[2], amount=10)
    recipe_2.save()


def test_public_requests(app, recipes, client):
    # getting public page responses
    without_user(app)

    pages = [
        {"path": "/ingredient/show/1/", "code": 302},  # redirect to login
        {"path": "/recipe/show/1/", "code": 404},
        {"path": "/recipe/show/2/", "code": 200},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"


def test_requests_logged_in(app, recipes, client):
    with_authenticated_user(app, username="user")

    pages = [
        {"path": "/ingredient/show/1/", "code": 200},
        {"path": "/ingredient/show/2/", "code": 200},
        {"path": "/ingredient/show/3/", "code": 200},
        {"path": "/ingredient/show/4/", "code": 404},
        {"path": "/recipe/show/1/", "code": 200},
        {"path": "/recipe/pdf/1/", "code": 200},
    ]

    for page in pages:
        assert client.get(page["path"]) == page["code"], f"path: {page['path']}"
