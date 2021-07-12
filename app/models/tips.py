from app import db

from app.helpers.base_mixin import BaseMixin


class Tip(db.Model, BaseMixin):
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
        tips = Tip.query.filter(Tip.is_approved).all()
        return tips

    @staticmethod
    def disapproved_tips():
        tips = Tip.query.filter(Tip.is_hidden).all()
        return tips

    @staticmethod
    def unapproved_tips():
        tips = Tip.query.filter_by(is_approved=False, is_hidden=False).all()
        return tips

    def approve(self):
        self.is_approved = True
        self.is_hidden = False
        self.save()

    def disapprove(self):
        self.is_approved = False
        self.is_hidden = True
        self.save()
