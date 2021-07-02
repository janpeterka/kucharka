from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class DailyPlanRecipeMixin:
    def add_recipe(self, recipe):
        order_index = self.daily_recipes[-1].order_index + 1

        daily_recipe = DailyPlanHasRecipe(
            recipe_id=recipe.id, daily_plan_id=self.id, order_index=order_index
        )

        daily_recipe.save()

        return daily_recipe

    def remove_daily_recipe(self, daily_recipe):

        if not self.can_current_user_edit:
            return False
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
