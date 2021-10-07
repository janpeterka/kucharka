from flask_security import current_user


class DailyPlanLoaderMixin:
    @staticmethod
    def load_by_date(date):
        from app.models.daily_plans import DailyPlan

        return DailyPlan.query.filter_by(date=date, created_by=current_user.id).first()

    @staticmethod
    def load_ingredient_amounts_for_daily_recipes(ids):
        from app import db
        from app.models.ingredients import Ingredient, IngredientCopy

        # i need to always have at least two ids for tuple to not have trailing coma
        if len(ids) < 2:
            ids.append(0)

        ids = tuple(ids)

        # TODO: change to SQlAlchemy Query to avoid SQL Injection risk and improve code (30)
        amounts_sql = f"""
                        SELECT
                            I.id AS ingredient_id,
                            -- CONCAT(R.id) AS recipe_ids,
                            SUM(RHI.amount * DPHR.portion_count) AS amount_sum
                        FROM
                            daily_plans_have_recipes AS DPHR
                            INNER JOIN recipes AS R ON
                                R.id = DPHR.recipe_id
                            INNER JOIN recipes_have_ingredients AS RHI ON
                                RHI.recipe_id = R.id
                            INNER JOIN ingredients AS I ON
                                I.id = RHI.ingredient_id
                        WHERE
                            DPHR.id IN {ids}
                        GROUP BY
                            I.id
                    """

        result = db.engine.execute(amounts_sql)

        ingredients = []

        for row in result:
            ingredient = IngredientCopy(Ingredient.load(row[0]))
            # ingredient.recipe_ids = row[1]
            ingredient.amount = row[1]
            ingredients.append(ingredient)

        return ingredients

    @staticmethod
    def load_ingredient_amounts_for_daily_plans(ids):
        # TODO: move this to ingredient model (90)
        from app import db
        from app.models.ingredients import Ingredient

        # i need to always have at least two ids for tuple to not have trailing coma
        if len(ids) < 2:
            ids.append(0)

        ids = tuple(ids)

        # TODO: change to SQlAlchemy Query to avoid SQL Injection risk and improve code (30)
        amounts_sql = f"""
                        SELECT
                            I.id AS ingredient_id,
                            -- CONCAT(R.id) AS recipe_ids,
                            SUM(RHI.amount * DPHR.portion_count) AS amount_sum
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

        return ingredients

    # @staticmethod
    # def load_by_date_range(date_from, date_to):
    #     from app.models.daily_plans import DailyPlan

    #     date_plans = DailyPlan.query.filter(
    #         DailyPlan.date.between(date_from, date_to)
    #     ).all()

    #     return date_plans

    # @staticmethod
    # def load_by_date_or_create(date):
    #     from app.models.daily_plans import DailyPlan

    #     daily_plan = DailyPlan.load_by_date(date)

    #     if daily_plan is None:
    #         daily_plan = DailyPlan(date=date)
    #         daily_plan.save()

    #     return daily_plan
