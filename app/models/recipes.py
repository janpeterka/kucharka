from unidecode import unidecode

from flask_security import current_user

from app import db

from app.helpers.item_mixin import ItemMixin

from app.models.ingredients import Ingredient
from app.models.recipes_have_ingredients import RecipeHasIngredient

from app.models.mixins.recipes.recipe_reactions import RecipeReactionMixin
from app.models.mixins.recipes.recipe_ingredients import RecipeIngredientMixin


class Recipe(db.Model, ItemMixin, RecipeReactionMixin, RecipeIngredientMixin):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.String())

    portion_count = db.Column(db.Integer)

    # recipe is not yet saved
    # is_draft = db.Column(db.Boolean, default=False)

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

    author = db.relationship("User", uselist=False, back_populates="recipes")

    category = db.relationship("RecipeCategory", uselist=False, backref="recipes")

    # LOADERS
    @staticmethod
    def load_all_public(
        ordered=True, exclude_mine=False, exclude_shopping=True
    ) -> list:
        recipes = Recipe.query.filter(Recipe.is_shared).all()
        recipes = [r for r in recipes if not (r.author.is_admin and r.name == "Nákup")]

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
            ingredient.set_additional_info(recipe)

        recipe.ingredients.sort(
            key=lambda x: (not x.is_measured, unidecode(x.name.lower()))
        )

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

    def duplicate(self):
        new = Recipe()

        new.name = self.name
        new.author = current_user
        new.description = self.description
        new.portion_count = self.portion_count
        new.ingredients = []
        for rhi in self.recipe_ingredients:
            new.add_ingredient(rhi.ingredient, amount=rhi.amount)

        new.save()
        return new

    def toggle_shared(self):
        self.is_shared = not self.is_shared
        self.edit()
        return self.is_shared

    # PERMISSIONS

    @property
    def can_current_user_show(self) -> bool:
        return current_user == self.author or current_user.is_admin or self.is_shared

    # PROPERTIES

    @property
    def is_shopping(self) -> bool:
        return True if self.author.is_admin and self.name == "Nákup" else False

    @property
    def is_used(self) -> bool:
        return True if self.daily_plans else False

    @property
    def is_visible(self) -> bool:
        return not self.is_draft

    @property
    def is_draft(self) -> bool:
        if self.is_shopping:
            return False

        return len(self.ingredients) == 0

    @property
    def has_zero_amount_ingredient(self) -> bool:
        for ingredient in self.recipe_ingredients:
            if ingredient.amount == 0 and ingredient.is_measured:
                return True

        return False

    @property
    def has_no_measurement_ingredient(self) -> bool:
        for ingredient in self.ingredient:
            if ingredient.without_measurement and ingredient.is_measured:
                return True

        return False

    @property
    def without_category(self) -> bool:
        if self.is_shopping:
            return False

        return self.category is None or self.category.name == "---"

    @property
    def concat_ingredients(self) -> str:
        return ", ".join([o.name for o in self.ingredients])

    @property
    def is_vegetarian(self) -> bool:
        return [i for i in self.ingredients if i.is_vegetarian] == self.ingredients

    @property
    def is_vegan(self) -> bool:
        return [i for i in self.ingredients if i.is_vegan] == self.ingredients

    @property
    def lactose_free(self) -> bool:
        return [i for i in self.ingredients if i.lactose_free] == self.ingredients

    @property
    def gluten_free(self) -> bool:
        return [i for i in self.ingredients if i.gluten_free] == self.ingredients
