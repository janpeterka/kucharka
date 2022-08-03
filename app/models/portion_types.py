from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class PortionType(BaseModel, BaseMixin):
    __tablename__ = "portion_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Float, nullable=False, default=1)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)

    author = db.relationship("User", uselist=False, back_populates="portion_types")
