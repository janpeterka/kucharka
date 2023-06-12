from unidecode import unidecode
from app.models.shopping import Shopping


class ShoppingListConstructor:
    def __init__(self, event):
        from app.services import DailyPlanIngredientCalculator

        self.event = event

        self.daily_plans = self.event.active_daily_plans
        self.split_recipes = self.event.daily_recipes_split_by_shopping

        self.ingredients = (
            DailyPlanIngredientCalculator.load_ingredient_amounts_for_daily_plans(
                self.daily_plans
            )
        )

    @property
    def _lasting_ingredients(self):
        return [i for i in self.ingredients if i.is_lasting]

    def get_lasting_shopping(self):
        # Nejdřív nákup před akcí - trvanlivé suroviny
        self._sort_ingredients(self._lasting_ingredients)

        # Tohle je pro rozpadnutí
        lasting_ingredients_shopping = Shopping()
        lasting_ingredients_shopping.shopping_list = self._lasting_ingredients
        lasting_ingredients_shopping.daily_recipes = self.event.daily_recipes
        lasting_ingredients_shopping.grouped_shopping_list = self._grouped_ingredients(
            self._lasting_ingredients
        )

        return lasting_ingredients_shopping

    def get_shoppings(self):
        from app.services import DailyPlanIngredientCalculator

        # a pak pro každý mezinákupový období
        shoppings = []
        for section in self.split_recipes:
            # If first event day begins with Shopping
            if not section:
                continue

            shopping = Shopping()
            shopping.daily_recipes = list(section)
            shopping.date = section[0].daily_plan.date
            shopping.is_shopping = section[0].is_shopping

            shopping_list = (
                DailyPlanIngredientCalculator.load_ingredient_amounts_for_daily_recipes(
                    section
                )
            )

            shopping_list = [i for i in shopping_list if not i.is_lasting]
            self._sort_ingredients(shopping_list)

            shopping.shopping_list = shopping_list
            shopping.grouped_shopping_list = self._grouped_ingredients(shopping_list)
            shoppings.append(shopping)

        return shoppings

    def _sort_ingredients(self, list_of_ingredients):
        list_of_ingredients.sort(
            key=lambda x: (
                getattr(x.category, "name", "ZZZ"),
                unidecode(x.name.lower()),
            )
        )

    def _grouped_ingredients(self, list_of_ingredients):
        unused_ingredient_categories = [i.category_name for i in list_of_ingredients]
        grouped_ingredients = {c: [] for c in unused_ingredient_categories}
        for i in list_of_ingredients:
            grouped_ingredients[i.category_name].append(i)

        return grouped_ingredients

    def get_amounts_for_shopping(self, shopping=None):
        used_recipes = [r.recipe for r in shopping.daily_recipes]
        recipe_ingredient_amounts = {}

        for ingredient in shopping.shopping_list:
            recipe_ingredient_amounts[ingredient.id] = {
                "name": ingredient.name,
                "recipes": {},
            }

            # Get list of recipes relevant for this shopping
            ingredient.event_recipes = [
                r for r in ingredient.recipes if r in used_recipes
            ]

            for event_recipe in ingredient.event_recipes:
                event_recipe.daily_plan_daily_recipes = [
                    dr
                    for dr in event_recipe.daily_plan_recipes
                    if dr in shopping.daily_recipes
                ]

                amount = sum(
                    (
                        ingredient.amount_by_recipe_or_zero(event_recipe)
                        * float(dr.portion_count)
                    )
                    for dr in event_recipe.daily_plan_daily_recipes
                )

                comment = ingredient.load_comment_by_recipe(event_recipe)

                recipe_ingredient_amounts[ingredient.id]["recipes"][event_recipe.id] = {
                    # "name": event_recipe.name,
                    "amount": amount,
                    "occurences": len(event_recipe.daily_plan_daily_recipes),
                    "comment": comment,
                }

        return recipe_ingredient_amounts
