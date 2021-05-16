# import math
import types

from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin


# from app.models.recipes import Recipe

# from app.models.recipes_have_ingredients import RecipeHasIngredient
from app.models.ingredients import Ingredient
from app.models.daily_plans_have_recipes import DailyPlanHasRecipe


class DailyPlan(db.Model, ItemMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    daily_recipes = db.relationship(
        "DailyPlanHasRecipe", back_populates="daily_plan", cascade="all,delete"
    )
    recipes = db.relationship(
        "Recipe", secondary="daily_plans_have_recipes", viewonly=True
    )

    event_id = db.Column(db.ForeignKey(("events.id")))
    event = db.relationship(
        "Event", backref=db.backref("daily_plans", cascade="all,delete")
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()
        # self.created_by = current_user.id

    @staticmethod
    def load_ingredient_amounts_for_daily_plans(ids, people_count):
        # i need to always have at least two ids for tuple to not have trailing coma
        if len(ids) < 2:
            ids.append(0)

        ids = tuple(ids)

        amounts_sql = f"""
                        SELECT
                            I.id AS ingredient_id,
                            -- CONCAT(R.id) AS recipe_ids,
                            SUM(RHI.amount) * {people_count} AS amount_sum
                        FROM
                            daily_plans AS DP
                            INNER JOIN daily_plans_have_recipes AS DPHR ON
                                DPHR.daily_plan_id = DP.id
                            INNER JOIN recipes AS R ON
                                R.id = DPHR.recipe_id
                            INNER JOIN recipes_have_ingredients AS RHI ON
                                RHI.recipe_id = R.id
                            INNER JOIN ingredients AS I ON
                                I.id = RHI.ingredient_id
                        WHERE
                            DP.id IN {ids}
                        GROUP BY
                            I.id
                    """

        result = db.engine.execute(amounts_sql)

        ingredients = []
        for row in result:
            ingredient = Ingredient.load(row[0])
            # ingredient.recipe_ids = row[1]
            ingredient.amount = row[1]
            ingredients.append(ingredient)

        # for ingredient in ingredients:
        #     ingredient.event_recipes = []
        #     for recipe_id in ingredient.recipe_ids:
        #         ingredient.event_recipes.append(Recipe.load(recipe_id))

        # for ingredient in ingredients:
        # ingredient.amount = ingredient.amount * float(people_count)

        return ingredients

    @staticmethod
    def load_by_date(date):
        # date_plan = DailyPlan.load_first_by_attribute("date", date)
        date_plan = DailyPlan.query.filter_by(
            date=date, created_by=current_user.id
        ).first()
        return date_plan

    @staticmethod
    def load_by_date_range(date_from, date_to):
        date_plans = DailyPlan.query.filter(
            DailyPlan.date.between(date_from, date_to)
        ).all()
        return date_plans

    @staticmethod
    def create_if_not_exists(date):
        DailyPlan.load_by_date_or_create(date)

    @staticmethod
    def load_by_date_or_create(date):
        daily_plan = DailyPlan.load_by_date(date)
        if daily_plan is None:
            daily_plan = DailyPlan(date=date, author=current_user)
            daily_plan.save()

        return daily_plan

    def add_recipe(self, recipe):
        order_index = len(self.daily_recipes) + 1

        daily_recipe = DailyPlanHasRecipe(
            recipe_id=recipe.id, daily_plan_id=self.id, order_index=order_index
        )

        daily_recipe.save()
        return daily_recipe

    def remove_daily_recipe_by_id(self, daily_recipe_id):
        selected_daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        if not self.can_current_user_edit:
            return False

        if selected_daily_recipe in self.daily_recipes:
            for daily_recipe in self.daily_recipes:
                if daily_recipe.order_index > selected_daily_recipe.order_index:
                    daily_recipe.order_index -= 1
                    daily_recipe.edit()
            selected_daily_recipe.delete()
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

    @property
    def weekday(self):
        from app.helpers.formaters import week_day

        return week_day(self.date)

    @property
    def name(self):
        return self.weekday
