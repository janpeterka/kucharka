from app import db
from sqlalchemy.orm import declared_attr


class Attendable:
    @declared_attr
    def attendees(self):
        return db.relationship(
            "Attendee",
            primaryjoin="Attendee.event_id == Event.id",
            back_populates="event",
            cascade="all, delete, delete-orphan",
        )

    @declared_attr
    def event_portion_types(self):
        return db.relationship(
            "EventPortionType",
            back_populates="event",
        )

    def event_portion_type(self, portion_type):
        from app.models import EventPortionType

        return EventPortionType.load_by_event_and_portion_type(self, portion_type)

    def attendees_with_portion_type(self, portion_type):
        return [a for a in self.attendees if a.portion_type == portion_type]

    @property
    def attendees_without_portion_type(self):
        return [a for a in self.attendees if not a.portion_type]

    @property
    def people_count_without_portion_type(self):
        return self.people_count - self.people_with_any_portion_type_count

    @property
    def count_addable_to_portion_type(self):
        return self.people_count_without_portion_type - len(
            self.attendees_without_portion_type
        )

    @property
    def people_with_any_portion_type_count(self):
        return sum([t.count for t in self.event_portion_types])

    @property
    def people_without_attendee_count(self):
        return self.people_count - len(self.attendees)

    @property
    def relative_portion_count(self):
        relative_portion_count = 0
        attendees_accounted_for_count = 0

        for event_portion_type in self.event_portion_types:
            relative_portion_count += (
                event_portion_type.count * event_portion_type.portion_type.size
            )
            attendees_accounted_for_count += event_portion_type.count

        relative_portion_count += self.people_count - attendees_accounted_for_count

        return relative_portion_count
