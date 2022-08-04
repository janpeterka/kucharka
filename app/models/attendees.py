from app import db, BaseModel
from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class Attendee(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "attendees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.ForeignKey("events.id"), nullable=False, index=True)
    portion_type_id = db.Column(db.ForeignKey("portion_types.id"))
    name = db.Column(db.String(255), nullable=False)

    labels = db.relationship("Label", secondary="attendees_have_labels")
    event = db.relationship("Event", back_populates="attendees")
    portion_type = db.relationship("PortionType")
