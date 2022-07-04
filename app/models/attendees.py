from app import db, BaseModel
from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class Attendee(BaseModel, BaseMixin, BasePresenter):
    _tablename__ = "attendees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.ForeignKey("events.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    portion_size_ratio = db.Column(db.Float())

    # dietary_labels =
    event = db.relationship("Event", back_populates="attendees")
