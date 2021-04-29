from unidecode import unidecode

from app import db

from app.helpers.base_mixin import BaseMixin


class Measurement(db.Model, BaseMixin):
    __tablename__ = "measurements"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    # LOADERS
    @staticmethod
    def load_all(ordered=True):
        measurements = Measurement.query.all()

        if ordered:
            measurements.sort(key=lambda x: unidecode(x.name.lower()))

        return measurements

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return True if self.ingredients else False
