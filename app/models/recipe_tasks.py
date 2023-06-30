from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin

from app.presenters import RecipeTaskPresenter


class RecipeTask(BaseModel, BaseMixin, RecipeTaskPresenter):
    __tablename__ = "recipe_tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
    days_before_cooking = db.Column(db.Integer)

    recipe_id = db.Column(db.ForeignKey("recipes.id"), nullable=False)

    recipe = db.relationship(
        "Recipe",
        backref=db.backref("tasks", cascade="all, delete, delete-orphan"),
        uselist=False,
    )

    def duplicate_to_recipe(self, recipe):
        task = RecipeTask(
            name=self.name,
            description=self.description,
            days_before_cooking=self.days_before_cooking,
        )
        task.recipe = recipe
        task.save()
        return task
