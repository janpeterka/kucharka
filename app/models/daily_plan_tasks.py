from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin

from app.presenters import ItemPresenter


class DailyPlanTask(BaseModel, BaseMixin, ItemPresenter):
    __tablename__ = "daily_plan_tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())

    daily_plan_id = db.Column(db.ForeignKey("daily_plans.id"), nullable=False)

    daily_plan = db.relationship(
        "DailyPlan",
        backref=db.backref("tasks", cascade="all, delete, delete-orphan"),
        uselist=False,
    )
