# import types
from app import db

from app.helpers.base_mixin import BaseMixin


class DailyPlanHasRecipe(db.Model, BaseMixin):
    __tablename__ = "daily_plans_have_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    daily_plan_id = db.Column(
        db.ForeignKey("daily_plans.id"), nullable=False, index=True
    )

    # amount = db.Column(db.Float, nullable=False)
    order_index = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, nullable=True, default=db.func.current_timestamp()
    )

    meal_type = db.Column(
        db.Enum(
            "snídaně",
            "dopolední svačina",
            "oběd",
            "odpolední svačina",
            "večeře",
            "programové",
            "jiné",
        )
    )

    daily_plan = db.relationship("DailyPlan")
    recipe = db.relationship("Recipe")

    # @property
    # def values(self):
    #     values = types.SimpleNamespace()
    #     metrics = ["calorie", "sugar", "fat", "protein"]
    #     for metric in metrics:
    #         total = getattr(self.recipe.totals, metric)
    #         if getattr(self, "amount", None) is not None:
    #             value = (total / self.recipe.totals.amount) * self.amount
    #         else:
    #             value = total
    #         setattr(values, metric, value)
    #     return values
