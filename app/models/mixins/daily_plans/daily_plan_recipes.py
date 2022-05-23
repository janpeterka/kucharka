from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class DailyPlanRecipeMixin:
    def add_recipe(self, recipe):
        order_index = len(self.daily_recipes) + 1

        daily_recipe = DailyPlanHasRecipe(
            recipe_id=recipe.id,
            daily_plan_id=self.id,
            order_index=order_index,
            portion_count=self.event.people_count,
        )

        daily_recipe.save()

        return daily_recipe

    def remove_daily_recipe(self, daily_recipe):
        if daily_recipe not in self.daily_recipes:
            return False

        daily_recipe.delete()
        self.reorder_recipes()

        return True

    def reorder_recipes(self):
        for i, recipe in enumerate(self.daily_recipes):
            recipe.order_index = i + 1

        self.save()

    # PROPERTIES

    @property
    def real_recipes(self):
        return [r for r in self.recipes if not r.is_shopping]
