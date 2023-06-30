import pytest
from tests.helpers import with_authenticated_user


@pytest.fixture
def recipe(app, db):
    from tests.factories import RecipeFactory, IngredientFactory, RecipeTaskFactory

    recipe = RecipeFactory()
    recipe.save()

    ingredient = IngredientFactory(name="First")
    ingredient.save()
    recipe.add_ingredient(ingredient)

    RecipeTaskFactory(name="First task", recipe_id=recipe.id).save()
    RecipeTaskFactory(name="Second task", recipe_id=recipe.id).save()

    return recipe


def test_recipe_duplication(app, recipe):
    with_authenticated_user(app, "user")

    recipe_copy = recipe.duplicate()

    assert recipe_copy.name == f"{recipe.name} (kopie)"
    assert len(recipe_copy.tasks) == len(recipe.tasks)
