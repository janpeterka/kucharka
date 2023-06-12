from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class RecipeHasIngredient(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "recipes_have_ingredients"

    recipe_id = db.Column(
        db.ForeignKey("recipes.id"), primary_key=True, nullable=False, index=True
    )
    ingredient_id = db.Column(
        db.ForeignKey("ingredients.id"), primary_key=True, nullable=False, index=True
    )
    amount = db.Column(db.Float)
    comment = db.Column(db.String(255))

    ingredient = db.relationship("Ingredient", back_populates="ingredient_recipes")
    recipe = db.relationship("Recipe", back_populates="recipe_ingredients")

    @staticmethod
    def load_by_recipe_and_ingredient(recipe, ingredient):
        return RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=ingredient.id
        ).first()

    @property
    def is_measured(self):
        return self.amount is not None
