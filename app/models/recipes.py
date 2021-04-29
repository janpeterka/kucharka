from unidecode import unidecode

from flask_login import current_user

from app import db

from app.helpers.item_mixin import ItemMixin

from app.models.ingredients import Ingredient
from app.models.recipes_have_ingredients import RecipeHasIngredient


class Recipe(db.Model, ItemMixin):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.Text)

    is_public = db.Column(db.Boolean, default=False)
    is_shared = db.Column(db.Boolean, default=False)

    recipe_ingredients = db.relationship("RecipeHasIngredient", back_populates="recipe")

    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredient.recipe_id), foreign(Ingredient.id) == RecipeHasIngredient.ingredient_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    author = db.relationship("User", uselist=False, backref="recipes")

    # LOADERS
    @staticmethod
    def load_all_public(ordered=True) -> list:
        recipes = Recipe.query.filter(Recipe.is_shared).all()
        print(recipes)
        # and_(Ingredient.is_shared, Ingredient.is_approved)

        if ordered:
            recipes.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)
        return recipes

    @staticmethod
    def load(recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            return None

        for ingredient in recipe.ingredients:
            ingredient.amount = round(ingredient.load_amount_by_recipe(recipe.id), 2)

        return recipe

    @staticmethod
    def load_by_ingredient(ingredient):
        recipes = Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.id == ingredient.id)
        ).all()
        return recipes

    @staticmethod
    def load_by_ingredient_and_user(ingredient, user):
        recipes = Recipe.load_by_ingredient(ingredient)
        private_recipes = [r for r in recipes if r.author == user]

        return private_recipes

    # Operations

    def create_and_save(self, recipe_ingredients):
        db.session.add(self)
        db.session.flush()

        # WIP - tohle je teď asi jinak

        for i in recipe_ingredients:
            i.recipe_id = self.id
            db.session.add(i)

        db.session.commit()
        return self.id

    def remove(self):
        # TODO: - to improve w/ orphan cascade (80)
        recipe_ingredients = RecipeHasIngredient.query.filter(
            RecipeHasIngredient.recipe_id == self.id
        )
        for i in recipe_ingredients:
            db.session.delete(i)

        db.session.delete(self)
        db.session.commit()
        return True

    def toggle_shared(self):
        self.is_shared = not self.is_shared
        self.edit()
        return self.is_shared

    # PERMISSIONS

    @property
    def can_current_user_show(self) -> bool:
        return current_user == self.author or current_user.is_admin or self.public

    # PROPERTIES

    @property
    def concat_ingredients(self) -> str:
        return ", ".join([o.name for o in self.ingredients])

    @property
    # @cache.cached(timeout=50, key_prefix="recipe_totals")
    def totals(self):
        import types
        import math

        totals = types.SimpleNamespace()
        metrics = ["calorie", "sugar", "fat", "protein"]

        totals.amount = 0

        for ingredient in self.ingredients:
            ingredient.amount = round(ingredient.load_amount_by_recipe(self.id), 2)
            for metric in metrics:
                value = getattr(totals, metric, 0)
                ing_value = getattr(ingredient, metric)
                setattr(totals, metric, value + (ingredient.amount * ing_value))

            totals.amount += ingredient.amount

        for metric in metrics:
            value = getattr(totals, metric)
            setattr(totals, metric, math.floor(value) / 100)

        totals.amount = math.floor(totals.amount)

        return totals
