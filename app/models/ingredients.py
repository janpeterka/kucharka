from unidecode import unidecode

from flask_security import current_user

from app import db, BaseModel

from app.helpers.item_mixin import ItemMixin
from app.models.recipes_have_ingredients import RecipeHasIngredient


class Ingredient(BaseModel, ItemMixin):
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

    def set_additional_info(self, recipe):
        self.amount = self.load_amount_by_recipe(recipe)
        self.comment = self.load_comment_by_recipe(recipe)
        self.is_measured = self.load_measured_by_recipe(recipe)

    # LOADERS
    @staticmethod
    def load_all_public(ordered=True, exclude_mine=False) -> list:
        ingredients = Ingredient.query.filter(Ingredient.is_public).all()

        if exclude_mine:
            ingredients = [r for r in ingredients if r.author != current_user]

        if ordered:
            ingredients.sort(key=lambda x: unidecode(x.name.lower()))

        return ingredients

    def load_amount_by_recipe(self, recipe) -> float:
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.amount

    def load_comment_by_recipe(self, recipe):
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.comment

    def load_measured_by_recipe(self, recipe):
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.is_measured

    # FUNCTIONS

    def publish(self):
        self.is_public = True
        self.edit()
        return self.is_public

    def unpublish(self):
        self.is_public = False
        self.edit()
        return self.is_public

    # PROPERTIES

    @property
    def is_lasting(self) -> bool:
        if self.category is None:
            return False
        else:
            return self.category.is_lasting

    @property
    def is_used(self) -> bool:
        return bool(self.recipes)

    @property
    def can_be_deleted(self) -> bool:
        return not self.is_used

    @property
    def without_category(self):
        return self.category is None or self.category.name == "---"

    @property
    def without_measurement(self):
        return self.measurement is None or self.measurement.name == "---"

    @property
    def can_edit_measurement(self):
        return True
        # return not self.is_used or self.without_measurement

    @property
    def alternative_measurement(self):
        if self.alternative_measurements:
            return self.alternative_measurements[0]
        else:
            return None

    @property
    def used_measurements(self):
        return [m.to_measurement for m in self.alternative_measurements] + [
            self.measurement
        ]

    @property
    def category_name(self):
        return getattr(self.category, "name", "---")

    # @property
    # def is_in_thousands(self):
    #     return self.measurement.thousand_fold and self.amount % 1000 != self.amount

    # PERMISSIONS

    def can_add(self, user) -> bool:
        return self.is_author(user) or self.is_public

    @property
    def can_current_user_add(self) -> bool:
        return self.can_add(current_user)

    def can_edit(self, user) -> bool:
        return (
            self.is_author(user)
            or user.is_admin
            or (self.is_public and user.is_application_manager)
        )

    def can_current_user_edit(self) -> bool:
        return self.can_edit(current_user)


class IngredientCopy:
    def __init__(self, ingredient):
        self.id = ingredient.id
        self.name = ingredient.name
        self.is_lasting = ingredient.is_lasting
        self.measurement = ingredient.measurement
        self.category = ingredient.category
        self.recipes = ingredient.recipes

    def load_amount_by_recipe(self, recipe) -> float:
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.amount

    def load_comment_by_recipe(self, recipe):
        rhi = RecipeHasIngredient.query.filter_by(
            recipe_id=recipe.id, ingredient_id=self.id
        ).first()
        return rhi.comment

    @property
    def category_name(self):
        return getattr(self.category, "name", "---")

    # CONTEXT PROCESSOR UTILITIES
    @property
    def link_to(self):
        from flask import url_for

        return f"<a data-turbo='false' href='{url_for('IngredientsView:show', id=self.id)}'>{self.name}</a>"
