from flask_security import current_user
from app.models import UserHasRecipeReaction


class RecipeReactionManager:
    def __init__(self, recipe):
        self.recipe = recipe

    def toggle_reaction(self, user=None):
        user = current_user if user is None else user

        if self.recipe.has_reaction is True:
            self.remove_reaction(user)
        else:
            self.add_reaction(user)

    def add_reaction(self, user):
        UserHasRecipeReaction(recipe=self.recipe, user=user).save()

    def remove_reaction(self, user):
        UserHasRecipeReaction.load_by_recipe_and_current_user(
            recipe=self.recipe
        ).delete()
