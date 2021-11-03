from app import db, BaseModel

from flask_security import current_user

from app.helpers.base_mixin import BaseMixin


class UserHasRecipeReaction(BaseModel, BaseMixin):
    __tablename__ = "users_have_recipes_reaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)

    recipe = db.relationship(
        "Recipe", backref=db.backref("reactions", cascade="all,delete")
    )
    user = db.relationship(
        "User", backref=db.backref("reactions", cascade="all,delete")
    )

    # LOADERS

    @staticmethod
    def load_by_recipe(recipe):
        return UserHasRecipeReaction.load_all_by_attribute("recipe_id", recipe.id)

    @staticmethod
    def load_by_recipe_and_user(recipe, user):
        return UserHasRecipeReaction.query.filter_by(
            recipe_id=recipe.id, user_id=user.id
        ).first()

    @staticmethod
    def load_by_recipe_and_current_user(recipe):
        return UserHasRecipeReaction.load_by_recipe_and_user(recipe, current_user)
