from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.helpers.general import classproperty, empty_object


class PortionType(BaseModel, BaseMixin):
    __tablename__ = "portion_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Float, nullable=False, default=1)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)

    author = db.relationship("User", uselist=False, back_populates="portion_types")

    @classproperty
    def default(cls):
        default_portion_type = empty_object()
        default_portion_type.size = 1
        default_portion_type.id = None

        return default_portion_type

    @property
    def is_default(self):
        return self.id is None
