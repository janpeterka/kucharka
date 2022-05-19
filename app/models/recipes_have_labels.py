from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class RecipeHasLabel(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "recipes_have_labels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False)
    label_id = db.Column(db.ForeignKey("labels.id"), nullable=False)
