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
        if rhi.amount != amount:
            rhi.amount = amount
            rhi.save()

        ingredient.amount = amount
        ingredient.refresh()

    def change_ingredient_comment(self, ingredient, comment):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        if comment != rhi.comment:
            rhi.comment = comment
            rhi.save()

        ingredient.comment = comment
        ingredient.refresh()

    def remove_ingredient(self, ingredient):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        if not rhi:
            return False

        rhi.delete()
        return True
