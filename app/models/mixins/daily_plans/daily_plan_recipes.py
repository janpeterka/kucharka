from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class DailyPlanRecipeMixin:
    def add_recipe(self, recipe):
        order_index = len(self.daily_recipes) + 1

        daily_recipe = DailyPlanHasRecipe(
            recipe_id=recipe.id, daily_plan_id=self.id, order_index=order_index
        )

        daily_recipe.save()
        return daily_recipe

    def remove_daily_recipe_by_id(self, daily_recipe_id):
        selected_daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        if not self.can_current_user_edit:
            return False

        if selected_daily_recipe in self.daily_recipes:
            for daily_recipe in self.daily_recipes:
                if daily_recipe.order_index > selected_daily_recipe.order_index:
                    daily_recipe.order_index -= 1
                    daily_recipe.edit()
            selected_daily_recipe.delete()
            return True
        else:
            return False

    # PROPERTIES

    @property
    def real_recipes(self):
        return [r for r in self.recipes if not r.is_shopping]
