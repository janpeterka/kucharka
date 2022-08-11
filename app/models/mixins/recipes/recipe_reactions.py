from flask_security import current_user
from app.models.users_have_recipes_reaction import UserHasRecipeReaction


class RecipeReactionMixin:
    def toggle_reaction(self, user=None):
        user = current_user if user is None else user

        if self.has_reaction is True:
            self.remove_reaction(user)
        else:
            self.add_reaction(user)

    def add_reaction(self, user):
        UserHasRecipeReaction(recipe=self, user=user).save()

    def remove_reaction(self, user):
        UserHasRecipeReaction.load_by_recipe_and_current_user(recipe=self).delete()

    @property
    def has_reaction(self) -> bool:
        reactions = UserHasRecipeReaction.load_by_recipe_and_current_user(self)

        return bool(reactions)
