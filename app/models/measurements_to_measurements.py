from app import db

from app.helpers.base_mixin import BaseMixin


class MeasurementToMeasurement(db.Model, BaseMixin):

    __tablename__ = "measurements_to_measurements"

    ingredient_id = db.Column(
        db.ForeignKey("ingredients.id"), primary_key=True, nullable=False
    )

    to_measurement_id = db.Column(
        db.ForeignKey("measurements.id"), primary_key=True, nullable=False
    )

    amount_from = db.Column(db.Float)
    amount_to = db.Column(db.Float, default=1)

    ingredient = db.relationship("Ingredient", backref="alternative_measurements")
    to_measurement = db.relationship("Measurement")
