from app.services import (
    # ShoppingListConstructor,
    # DailyPlanIngredientCalculator,
    EventManager,
)

from tests.factories import EventFactory
from tests.helpers import with_authenticated_user


# WIP
def test_ingredient_calculator(app, client, db):
    with_authenticated_user(app, username="user")

    event = EventFactory(length=3)
    event.save()

    EventManager(event).add_new_daily_plans()

    # TODO: this doesn't work in
    # ingredients = DailyPlanIngredientCalculator.load_ingredient_amounts_for_daily_recipes(event.daily_recipes)
    # print(ingredients)
