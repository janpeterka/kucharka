from sqlalchemy.ext.hybrid import hybrid_property

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class RecipeHasIngredient(BaseModel, BaseMixin):
    """Recipe-Ingredient connection class

    Extends:
        Base

    Variables:
        __tablename__ {str} -- [description]
        recipe_id {int} -- [description]
        ingredient_id {int} -- [description]
        amount {int} -- [description]
        ingredients {relationship} -- [description]
        recipes {relationship} -- [description]
    """

    __tablename__ = "recipes_have_ingredients"

    recipe_id = db.Column(
        db.ForeignKey("recipes.id"), primary_key=True, nullable=False, index=True
    )
    ingredient_id = db.Column(
        db.ForeignKey("ingredients.id"), primary_key=True, nullable=False, index=True
    )
    amount = db.Column(db.Float, nullable=False, default=0)
    comment = db.Column(db.String(255))
    _is_measured = db.Column(db.Boolean, default=True)

    ingredient = db.relationship("Ingredient", back_populates="ingredient_recipes")
    recipe = db.relationship("Recipe", back_populates="recipe_ingredients")

    @staticmethod
    def load_by_recipe_and_ingredient(recipe, ingredient):
        return RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=ingredient.id
        ).first()

    @hybrid_property
    def is_measured(self):
        return self._is_measured is not False

    @is_measured.setter
    def is_measured(self, is_measured):
        self._is_measured = is_measured
