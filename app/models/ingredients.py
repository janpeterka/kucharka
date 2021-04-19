from sqlalchemy.ext.hybrid import hybrid_property

from flask_login import current_user

from app import db

from app.helpers.item_mixin import ItemMixin
from app.models.recipes_have_ingredients import RecipeHasIngredient


class Ingredient(db.Model, ItemMixin):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("user.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.Text)
    measurement = db.Column(db.Enum("gram", "kus", "mililtr"), nullable=False, default="gram")

    calorie = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    fat = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))
    protein = db.Column(db.Float, nullable=False, server_default=db.text("'0'"))

    ingredient_recipes = db.relationship("RecipeHasIngredient", back_populates="ingredient")

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipeHasIngredient.ingredient_id), foreign(Recipe.id) == RecipeHasIngredient.recipe_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    author = db.relationship("User", uselist=False, backref="ingredients")

    # LOADERS

    def load_amount_by_recipe(self, recipe_id) -> float:
        print([r for r in self.ingredient_recipes if r.recipe_id == recipe_id][0].amount) 
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe_id, ingredient_id=self.id
        ).first()
        return rhi.amount

    # def fill_from_json(self, json_ing):
    #     if "fixed" in json_ing:
    #         self.fixed = json_ing["fixed"]
    #     if "main" in json_ing:
    #         self.main = json_ing["main"]

    #     if "amount" in json_ing:
    #         self.amount = float(json_ing["amount"]) / 100  # from grams per 100g

    #     if "min" in json_ing and len(json_ing["min"]) > 0:
    #         self.min = float(json_ing["min"])

    #     if "max" in json_ing and len(json_ing["max"]) > 0:
    #         self.max = float(json_ing["max"])

    def is_author(self, user) -> bool:
        return self.author == user

    @hybrid_property
    def is_current_user_author(self) -> bool:
        return self.is_author(current_user)

    def can_add(self, user) -> bool:
        return self.is_author(user)

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)

    @property
    def is_used(self) -> bool:
        return True if self.recipes else False
