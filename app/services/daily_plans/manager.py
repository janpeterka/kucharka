class DailyPlanManager:
    def __init__(self, daily_plan):
        self.daily_plan = daily_plan

    def add_recipe(self, recipe):
        from app.models import DailyPlanRecipe

        order_index = len(self.daily_plan.daily_recipes) + 1

        daily_recipe = DailyPlanRecipe(
            recipe_id=recipe.id,
            daily_plan_id=self.daily_plan.id,
            order_index=order_index,
            portion_count=self.daily_plan.event.people_count,
        )

        daily_recipe.save()

        return daily_recipe

    def add_shopping(self):
        from app.models import Recipe

        return self.add_recipe(Recipe.load_shopping())

    def remove_daily_recipe(self, daily_recipe):
        if daily_recipe not in self.daily_plan.daily_recipes:
            return False

        daily_recipe.delete()
        self.reorder_recipes()

    def reorder_recipes(self):
        for i, recipe in enumerate(self.daily_plan.daily_recipes):
            recipe.order_index = i + 1

        self.daily_plan.save()
