from datetime import timedelta

# from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin


class Event(db.Model, ItemMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    people_count = db.Column(db.Integer)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, backref="events")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()
        # self.created_by = current_user.id

    @property
    def duration(self):
        return (self.date_to - self.date_from).days

    @property
    def days(self):
        return [
            self.date_from + timedelta(days=x)
            for x in range((self.date_to - self.date_from).days + 1)
        ]

    @property
    def recipes(self):
        recipes = []
        for daily_plan in self.daily_plans:
            recipes = recipes + daily_plan.real_recipes

        return recipes

    @property
    def recipes_without_duplicated(self):
        from app.helpers.general import list_without_duplicated

        return list_without_duplicated(self.recipes)

    @property
    def daily_recipes(self):
        daily_recipes = []
        for daily_plan in self.daily_plans:
            daily_recipes = daily_recipes + daily_plan.daily_recipes

        return daily_recipes

    @property
    def daily_recipes_split_by_shopping(self):
        daily_recipes = self.daily_recipes
        split_recipes = []

        shopping_indexes = [0]
        for i, recipe in enumerate(daily_recipes):
            if recipe.is_shopping:
                shopping_indexes.append(i)

        shopping_indexes.append(len(daily_recipes))

        for i in range(len(shopping_indexes) - 1):
            i_from = shopping_indexes[i]
            i_to = shopping_indexes[i + 1]

            split_recipes.append(daily_recipes[i_from:i_to])

        return split_recipes

    @property
    def zero_amount_ingredient_recipes(self):
        return [r for r in self.recipes if r.has_zero_amount_ingredient]

    @property
    def no_measurement_ingredient_recipes(self):
        return [r for r in self.recipes if r.has_no_measurement_ingredient]

    @property
    def recipes_without_category(self):
        return [r for r in self.recipes if r.without_category]

    @property
    def empty_recipes(self):
        return [r for r in self.recipes if r.is_draft]
