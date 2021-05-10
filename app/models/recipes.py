from unidecode import unidecode

from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin

from app.models.ingredients import Ingredient
from app.models.recipes_have_ingredients import RecipeHasIngredient
from app.models.users_have_recipes_reaction import UserHasRecipeReaction


class Recipe(db.Model, ItemMixin):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.Text)

    portion_count = db.Column(db.Integer)

    # recipe is not yet saved
    is_draft = db.Column(db.Boolean, default=False)

    # recipe is from database of approved recipes
    # is_public = db.Column(db.Boolean, default=False)
    # recipes is personal, but shared publicly. can change or disappear
    is_shared = db.Column(db.Boolean, default=False)
    # recipe is hidden from personal and public lists
    is_hidden = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.ForeignKey("recipe_categories.id"))

    recipe_ingredients = db.relationship("RecipeHasIngredient", back_populates="recipe")

    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredient.recipe_id), foreign(Ingredient.id) == RecipeHasIngredient.ingredient_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    daily_plans = db.relationship(
        "DailyPlan",
        primaryjoin="and_(Recipe.id == remote(DailyPlanHasRecipe.recipe_id), foreign(DailyPlan.id) == DailyPlanHasRecipe.daily_plan_id)",
        viewonly=True,
    )

    author = db.relationship("User", uselist=False, backref="recipes")

    category = db.relationship("RecipeCategory", uselist=False, backref="recipes")

    # LOADERS
    @staticmethod
    def load_all_public(ordered=True, exclude_mine=False) -> list:
        recipes = Recipe.query.filter(Recipe.is_shared).all()

        if exclude_mine:
            recipes = [r for r in recipes if r.author != current_user]

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

    def toggle_reaction(self, user=None):
        user = current_user if user is None else user

        if self.has_reaction is True:
            self.remove_reaction(user)
        else:
            self.add_reaction(user)

    def add_reaction(self, user):
        UserHasRecipeReaction(recipe=self, user=user).save()

    def remove_reaction(self, user):
        UserHasRecipeReaction.load_by_recipe_and_current_user(recipe=self).remove()

    @property
    def has_reaction(self):
        reactions = UserHasRecipeReaction.load_by_recipe_and_current_user(self)
        return bool(reactions)

    def add_ingredient(self, ingredient, amount=None):
        rhi = RecipeHasIngredient()
        rhi.ingredient = ingredient
        if amount:
            rhi.amount = amount

        self.recipe_ingredients.append(rhi)
        self.save()

    def remove_ingredient(self, ingredient):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        rhi.delete()

    def change_ingredient_amount(self, ingredient, amount):
        rhi = RecipeHasIngredient.load_by_recipe_and_ingredient(self, ingredient)
        rhi.amount = amount
        rhi.save()

    # PERMISSIONS

    @property
    def can_current_user_show(self) -> bool:
        return current_user == self.author or current_user.is_admin or self.is_shared

    # PROPERTIES

    @property
    def is_used(self):
        return True if self.daily_plans else False

    @property
    def is_visible(self):
        return not self.is_draft

    @property
    def concat_ingredients(self) -> str:
        return ", ".join([o.name for o in self.ingredients])

    @property
    def is_vegetarian(self):
        return [i for i in self.ingredients if i.is_vegetarian] == self.ingredients

    @property
    def is_vegan(self):
        return [i for i in self.ingredients if i.is_vegan] == self.ingredients

    @property
    def lactose_free(self):
        return [i for i in self.ingredients if i.lactose_free] == self.ingredients

    @property
    def gluten_free(self):
        return [i for i in self.ingredients if i.gluten_free] == self.ingredients

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
