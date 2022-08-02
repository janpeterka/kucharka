class DailyRecipeManager:
    def __init__(self, daily_recipe):
        self.daily_recipe = daily_recipe

    def change_order(self, order_type):
        coef = 1 if order_type == "up" else -1

        for daily_recipe in self.daily_recipe.daily_plan.daily_recipes:
            if daily_recipe.order_index == self.daily_recipe.order_index - (1 * coef):
                daily_recipe.order_index += 1 * coef
                daily_recipe.edit()

                self.daily_recipe.order_index -= 1 * coef
                self.daily_recipe.edit()
                return
