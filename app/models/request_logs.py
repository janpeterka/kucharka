from sqlalchemy.sql import func

from app import db, BaseModel
from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class RequestLog(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=func.now())

    url = db.Column(db.String(255))
    remote_addr = db.Column(db.String(255))
    duration = db.Column(db.Float(precision=4))

    item_type = db.Column(db.String(255))
    item_id = db.Column(db.Integer)

    user_id = db.Column(db.ForeignKey(("users.id")), index=True)
    user = db.relationship("User")
