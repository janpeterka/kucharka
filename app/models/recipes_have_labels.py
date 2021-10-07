from app import db, BaseModel

# from flask_security import current_user

from app.helpers.base_mixin import BaseMixin


class RecipeHasLabel(BaseModel, BaseMixin):
    __tablename__ = "recipes_have_labels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False)
    label_id = db.Column(db.ForeignKey("labels.id"), nullable=False)
