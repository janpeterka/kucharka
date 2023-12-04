# import types
from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter

# from sqlalchemy.ext.hybrid import hybrid_property


class DailyPlanRecipe(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "daily_plans_have_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    daily_plan_id = db.Column(
        db.ForeignKey("daily_plans.id"), nullable=False, index=True
    )

    position = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, nullable=True, default=db.func.current_timestamp()
    )

    portion_count = db.Column(db.Float, nullable=False, default=0)

    meal_type = db.Column(
        db.Enum(
            "snídaně",
            "dopolední svačina",
            "oběd",
            "odpolední svačina",
            "večeře",
            "programové",
            "jiné",
            "nákup",
        )
    )

    daily_plan = db.relationship("DailyPlan")
    recipe = db.relationship("Recipe", backref="daily_plan_recipes")

    @property
    def tasks(self):
        from app.models import RecipeTask

        return RecipeTask.load_all(recipe_id=self.recipe_id)

    def duplicate(self):
        daily_recipe = DailyPlanRecipe()
        daily_recipe.recipe_id = self.recipe_id
        daily_recipe.daily_plan_id = self.daily_plan_id
        daily_recipe.position = self.position
        daily_recipe.portion_count = self.portion_count
        daily_recipe.meal_type = self.meal_type

        daily_recipe.save()

        return daily_recipe

    @property
    def is_shopping(self) -> bool:
        return self.recipe.name == "Nákup" or self.meal_type == "nákup"

    @property
    def is_first_recipe(self) -> bool:
        return self == self.daily_plan.first_recipe

    @property
    def is_last_recipe(self) -> bool:
        return self == self.daily_plan.last_recipe

    def can_edit(self, user) -> bool:
        return self.daily_plan.event.can_edit(user)
