from unidecode import unidecode

from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin
from app.models.recipes_have_ingredients import RecipeHasIngredient


class Ingredient(db.Model, ItemMixin):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.Text)
    measurement_id = db.Column(db.ForeignKey("measurements.id"))
    category_id = db.Column(db.ForeignKey("ingredient_categories.id"))

    calorie = db.Column(db.Float, server_default=db.text("'0'"))
    sugar = db.Column(db.Float, server_default=db.text("'0'"))
    fat = db.Column(db.Float, server_default=db.text("'0'"))
    protein = db.Column(db.Float, server_default=db.text("'0'"))

    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    lactose_free = db.Column(db.Boolean, default=False)
    gluten_free = db.Column(db.Boolean, default=False)

    is_public = db.Column(db.Boolean, default=False)
    # is_approved = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(255), default="user")

    ingredient_recipes = db.relationship(
        "RecipeHasIngredient", back_populates="ingredient"
    )

    recipes = db.relationship(
        "Recipe",
        primaryjoin="and_(Ingredient.id == remote(RecipeHasIngredient.ingredient_id), foreign(Recipe.id) == RecipeHasIngredient.recipe_id)",
        viewonly=True,
        order_by="Recipe.name",
    )

    author = db.relationship("User", uselist=False, backref="ingredients")
    measurement = db.relationship("Measurement", uselist=False, backref="ingredients")
    category = db.relationship(
        "IngredientCategory", uselist=False, backref="ingredients"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    # LOADERS
    @staticmethod
    def load_all_public(ordered=True, exclude_mine=False) -> list:
        ingredients = Ingredient.query.filter(Ingredient.is_public).all()
        # and_(Ingredient.is_public, Ingredient.is_approved)

        if exclude_mine:
            ingredients = [r for r in ingredients if r.author != current_user]

        if ordered:
            ingredients.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)
        return ingredients

    def load_amount_by_recipe(self, recipe) -> float:
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.amount

    def load_amount_by_recipe_id(self, recipe_id) -> float:
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe_id, ingredient_id=self.id
        ).first()
        return rhi.amount

    def load_comment_by_recipe(self, recipe):
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.comment

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return True if self.recipes else False

    @property
    def without_category(self):
        return self.category is None or self.category.name == "---"

    @property
    def without_measurement(self):
        return self.measurement is None or self.measurement.name == "---"

    # @property
    def can_edit_measurement(self):
        return True
        # return not self.is_used or self.without_measurement

    # PERMISSIONS

    def can_add(self, user) -> bool:
        return self.is_author(user) or self.is_public

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)
