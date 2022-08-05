from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class EventPortionType(BaseModel, BaseMixin):
    __tablename__ = "event_has_portion_type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    count = db.Column(db.Integer, nullable=False, default=0)
    event_id = db.Column(db.ForeignKey("events.id"), nullable=False)
    portion_type_id = db.Column(db.ForeignKey("portion_types.id"), nullable=False)

    event = db.relationship(
        "Event", uselist=False, back_populates="event_portion_types", viewonly=True
    )
    portion_type = db.relationship("PortionType", uselist=False)

    @staticmethod
    def load_by_event_and_portion_type(event, portion_type):
        return EventPortionType.query.filter_by(
            event_id=event.id, portion_type_id=portion_type.id
        ).first()

    @property
    def attendees(self):
        return [a for a in self.event.attendees if a.portion_type == self]
