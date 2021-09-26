from app import db, BaseModel

# from flask_security import current_user

from app.helpers.base_mixin import BaseMixin


class IngredientHasLabel(BaseModel, BaseMixin):
    __tablename__ = "ingredients_have_labels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    ingredient_id = db.Column(db.ForeignKey("ingredients.id"), nullable=False)
    label_id = db.Column(db.ForeignKey("labels.id"), nullable=False)

    # ingredient = db.relationship("Ingredient", backref="ingredient_labels")
    # label = db.relationship("Label", backref="ingredient_labels")

    # # LOADERS

    # @staticmethod
    # def load_by_ingredient(ingredient):
    #     return IngredientHasLabel.load_all_by_attribute("ingredient_id", ingredient.id)
