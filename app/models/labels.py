from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class Label(BaseModel, BaseMixin):
    __tablename__ = "labels"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    visible_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    category_id = db.Column(db.ForeignKey("label_categories.id"))
    category = db.relationship("LabelCategory", uselist=False, backref="labels")

    color = db.Column(db.String(255))

    def __str__(self):
        if self.visible_name:
            return self.visible_name
        else:
            return self.name

    @staticmethod
    def load_by_category_name(category_name):
        from app.models.label_categories import LabelCategory

        return [
            label
            for label in Label.load_all()
            if label.category == LabelCategory.load_by_name(category_name)
        ]

    @staticmethod
    def load_dietary():
        return Label.load_by_category_name("dietary")

    @staticmethod
    def load_difficulty():
        return Label.load_by_category_name("difficulty")

    @property
    def icon_name(self) -> str:
        return self.name
