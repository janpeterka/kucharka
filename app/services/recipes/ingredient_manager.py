class RecipeIngredientManager:
    def __init__(self, recipe):
        self.recipe = recipe

    def update_ingredient_amounts(self, old_portion_count, new_portion_count):
        for recipe_ingredient in self.recipe.recipe_ingredients:
            old_total_amount = recipe_ingredient.amount * old_portion_count
            recipe_ingredient.amount = old_total_amount / new_portion_count
            recipe_ingredient.edit()
