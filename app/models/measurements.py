from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class Measurement(BaseModel, BaseMixin):
    __tablename__ = "measurements"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    suffix = db.Column(db.String(20))
    sorting_priority = db.Column(db.Integer(), server_default="0")

    thousand_fold = db.Column(db.String(20))

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return bool(self.ingredients)

    @property
    def count(self) -> int:
        return len(self.ingredients)
