from sqlalchemy.sql import func

from app.helpers.base_mixin import BaseMixin

from app import db


class RequestLog(db.Model, BaseMixin):
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

    # @staticmethod
    # def load_by_like(attribute=None, pattern=None):
    #     if not hasattr(RequestLog, attribute):
    #         raise AttributeError

    #     return RequestLog.query.filter(
    #         getattr(RequestLog, attribute).like(f"%{pattern}%")
    #     ).all()
