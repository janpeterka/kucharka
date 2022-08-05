from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class AttendeeHasLabel(BaseModel, BaseMixin):
    __tablename__ = "attendees_have_labels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendee_id = db.Column(db.ForeignKey("attendees.id"), nullable=False, index=True)
    label_id = db.Column(db.ForeignKey("labels.id"), nullable=False, index=True)

    attendee = db.relationship("Attendee", back_populates="attendee_labels")
    label = db.relationship("Label")
