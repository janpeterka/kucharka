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
            recipes = recipes + daily_plan.recipes
        return recipes
