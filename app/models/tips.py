from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class Tip(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "tips"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)

    is_approved = db.Column(db.Boolean(), default=False, nullable=False)
    is_hidden = db.Column(db.Boolean(), default=False, nullable=False)

    author = db.relationship("User", uselist=False, backref="tips")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    @staticmethod
    def approved_tips():
        return Tip.query.filter(Tip.is_approved).all()

    @staticmethod
    def disapproved_tips():
        return Tip.query.filter(Tip.is_hidden).all()

    @staticmethod
    def unapproved_tips():
        return Tip.query.filter_by(is_approved=False, is_hidden=False).all()

    def approve(self):
        self.is_approved = True
        self.is_hidden = False
        self.save()

    def disapprove(self):
        self.is_approved = False
        self.is_hidden = True
        self.save()
