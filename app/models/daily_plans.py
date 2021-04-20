import math
import types

from flask_login import current_user

from app import db

from app.helpers.base_mixin import BaseMixin

from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class DailyPlan(db.Model, BaseMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    daily_recipes = db.relationship("DailyPlanHasRecipe", back_populates="daily_plan")
    # recipes = db.relationship("Recipe", secondary="daily_plan_daily_recipes")

    @staticmethod
    def load_by_date(date):
        # date_plan = DailyPlan.load_first_by_attribute("date", date)
        date_plan = DailyPlan.query.filter_by(
            date=date, created_by=current_user.id
        ).first()
        return date_plan

    @staticmethod
    def load_by_date_or_create(date):
        daily_plan = DailyPlan.load_by_date(date)
        if daily_plan is None:
            daily_plan = DailyPlan(date=date, author=current_user)
            daily_plan.save()

        return daily_plan

    def add_recipe(self, recipe):
        order_index = len(self.daily_recipes) + 1

        dphr = DailyPlanHasRecipe(
            recipe_id=recipe.id,
            daily_plan_id=self.id,
            order_index=order_index,
        )

        dphr.save()

    def remove_daily_recipe_by_id(self, daily_recipe_id):
        # TODO - jenom pokud je fakt v tomhle daily_planu
        selected_daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)

        if selected_daily_recipe in self.daily_recipes:
            for daily_recipe in self.daily_recipes:
                if daily_recipe.order_index > selected_daily_recipe.order_index:
                    daily_recipe.order_index -= 1
                    daily_recipe.edit()
            selected_daily_recipe.remove()
            return True
        else:
            return False

    def change_order(self, daily_recipe_id, order_type):
        # WIP - WTF is this?
        coef = 1 if order_type == "up" else -1

        selected_daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)

        for daily_recipe in self.daily_recipes:
            if daily_recipe.order_index == selected_daily_recipe.order_index - (
                1 * coef
            ):
                daily_recipe.order_index += 1 * coef
                daily_recipe.edit()

                selected_daily_recipe.order_index -= 1 * coef
                selected_daily_recipe.edit()
                return

    @property
    def totals(self):
        totals = types.SimpleNamespace()
        print(totals)

        metrics = ["calorie", "sugar", "fat", "protein"]
        for metric in metrics:
            setattr(totals, metric, 0)

        totals.amount = 0

        for daily_recipe in self.daily_recipes:
            recipe = daily_recipe.recipe
            recipe.amount = recipe.totals.amount

            for metric in metrics:
                value = getattr(totals, metric)
                recipe_value = getattr(recipe.totals, metric)
                setattr(totals, metric, value + recipe_value)
            totals.amount += recipe.amount

        return totals

    @property
    def is_active(self):
        return len(self.daily_recipes) > 0
