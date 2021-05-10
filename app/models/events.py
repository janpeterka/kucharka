# import types

# from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin

# from app.models.recipes_have_ingredients import RecipeHasIngredient
# from app.models.ingredients import Ingredient
# from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class Event(db.Model, ItemMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, backref="events")
