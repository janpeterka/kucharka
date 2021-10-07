from app.models.recipes_have_ingredients import RecipeHasIngredient


class RecipeIngredientMixin:
    def add_ingredient(self, ingredient, amount=None):
        rhi = RecipeHasIngredient()
        rhi.ingredient = ingredient

        if amount:
            rhi.amount = amount

        self.recipe_ingredients.append(rhi)
        self.save()

    def change_ingredient_amount(self, ingredient, amount):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        rhi.amount = amount
        rhi.save()

    def change_ingredient_comment(self, ingredient, comment):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        rhi.comment = comment
        rhi.save()

    def change_ingredient_measured(self, ingredient, measured):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        rhi.is_measured = measured
        if not rhi.is_measured and rhi.amount:
            rhi.amount = 0
        rhi.save()

    def remove_ingredient(self, ingredient):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        if not rhi:
            return False

        rhi.delete()
        return True
