from unidecode import unidecode

from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import current_user

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.helpers.general import list_without_duplicated

from app.presenters import RecipePresenter

from app.models.mixins.recipes.recipe_ingredients import RecipeIngredientMixin


class Recipe(BaseModel, BaseMixin, RecipeIngredientMixin, RecipePresenter):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    description = db.Column(db.String(255))

    portion_count = db.Column(db.Integer)

    # recipe is not yet saved
    # is_draft = db.Column(db.Boolean, default=False)

    # recipe is from database of approved recipes
    # is_public = db.Column(db.Boolean, default=False)

    # recipe is personal, but shared publicly. can change or disappear
    is_shared = db.Column(db.Boolean, default=False)

    # recipe is hidden from personal and public lists
    is_hidden = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.ForeignKey("recipe_categories.id"))

    recipe_ingredients = db.relationship("RecipeHasIngredient", back_populates="recipe")

    ingredients = db.relationship(
        "Ingredient",
        secondary="recipes_have_ingredients",
        primaryjoin="Recipe.id == RecipeHasIngredient.recipe_id",
        viewonly=True,
        order_by="Ingredient.name",
    )

    daily_plans = db.relationship(
        "DailyPlan",
        secondary="daily_plans_have_recipes",
        primaryjoin="Recipe.id == DailyPlanRecipe.recipe_id",
        viewonly=True,
    )

    author = db.relationship("User", uselist=False, back_populates="recipes")

    category = db.relationship(
        "RecipeCategory", uselist=False, backref="recipes", lazy="joined"
    )

    labels = db.relationship(
        "Label",
        secondary="recipes_have_labels",
        primaryjoin="Recipe.id == RecipeHasLabel.recipe_id",
        order_by="Label.id",
    )

    # LOADERS
    @staticmethod
    def load_all_public(
        ordered=True, exclude_mine=False, exclude_shopping=True
    ) -> list:
        recipes = Recipe.query.filter(Recipe.is_shared).all()
        recipes = [r for r in recipes if not (r.is_shopping)]

        if exclude_mine:
            recipes = [r for r in recipes if r.author != current_user]

        if ordered:
            recipes.sort(key=lambda x: unidecode(x.name.lower()), reverse=False)

        return recipes

    @staticmethod
    def load_all_public_with_image() -> list:
        recipes = Recipe.load_all_public()
        recipes = [r for r in recipes if r.has_image]

        return recipes

    @staticmethod
    def load(recipe_id):
        from app.models import LabelCategory

        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            return None

        for ingredient in recipe.ingredients:
            ingredient.set_additional_info(recipe)

        recipe.ingredients.sort(
            key=lambda x: (
                x.is_measured,
                x.sorting_priority,
                x.amount,
                unidecode(x.name.lower()),
            ),
            reverse=True,
        )

        for category in LabelCategory.load_all():
            labels = [label for label in recipe.labels if label.category == category]
            if category.allow_multiple:
                setattr(recipe, f"{category.name}_labels", labels)
            else:
                label = labels[0] if labels else None
                setattr(recipe, f"{category.name}_label", label)

        return recipe

    def reload(self):
        return Recipe.load(self.id)

    @staticmethod
    def load_by_ingredient(ingredient):
        from app.models import Ingredient

        return Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.id == ingredient.id)
        ).all()

    @staticmethod
    def load_by_ingredient_and_user(ingredient, user):
        recipes = Recipe.load_by_ingredient(ingredient)

        return [r for r in recipes if r.author == user]

    @staticmethod
    def load_shopping():
        return Recipe.load_by_name("Nákup")

    # Operations
    def remove(self):
        from app.models import RecipeHasIngredient

        # TODO: to improve w/ orphan cascade (80)
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

        new.name = f"{self.name} (kopie)"
        new.author = current_user
        new.description = self.description
        new.portion_count = self.portion_count
        new.category = self.category
        new.labels = self.labels
        new.ingredients = []
        for rhi in self.recipe_ingredients:
            new.add_ingredient(rhi.ingredient, amount=rhi.amount)

        new.save()

        for task in self.tasks:
            task.duplicate_to_recipe(new)

        return new

    def share(self):
        if not self.is_shared:
            self.is_shared = True
            self.edit()

    def toggle_shared(self):
        self.is_shared = not self.is_shared
        self.edit()
        return self.is_shared

    # PERMISSIONS

    def can_view(self, user) -> bool:
        return (
            self.is_shared
            or self.is_in_shared_event
            or (user.is_authenticated and self in user.role_event_recipes)
            or user == self.author
            or (user.is_authenticated and user.has_permission("see-other"))
        )

    # PROPERTIES
    @property
    def has_reaction(self) -> bool:
        from app.models import UserHasRecipeReaction

        reactions = UserHasRecipeReaction.load_by_recipe_and_current_user(self)

        return bool(reactions)

    @property
    def is_shopping(self) -> bool:
        return self.author.has_role("admin") and self.name == "Nákup"

    @property
    def is_used(self) -> bool:
        return bool(self.daily_plans)

    @property
    def is_visible(self) -> bool:
        return not self.is_draft and not self.is_shopping

    @property
    def events(self) -> list:
        events = [dp.event for dp in self.daily_plans]
        return list_without_duplicated(events)

    @property
    def shared_events(self) -> list:
        return [event for event in self.events if event.is_shared]

    @property
    def is_in_shared_event(self) -> bool:
        return bool(self.shared_events)

    @property
    def is_draft(self) -> bool:
        if self.is_shopping:
            return False

        return len(self.ingredients) == 0

    @property
    def unused_personal_ingredients(self) -> list:
        return [
            i for i in current_user.personal_ingredients if i not in self.ingredients
        ]

    @property
    def unused_public_ingredients(self) -> list:
        from app.models import Ingredient

        return [i for i in Ingredient.load_all_public() if i not in self.ingredients]

    @property
    def zero_amount_ingredients(self) -> list:
        return [
            ri.ingredient
            for ri in self.recipe_ingredients
            if ri.is_measured and ri.amount == 0
        ]

    @property
    def has_zero_amount_ingredient(self) -> bool:
        return len(self.zero_amount_ingredients) > 0

    @property
    def no_measurement_ingredients(self) -> list:
        return [i for i in self.ingredients if i.is_measured and i.without_measurement]

    @property
    def has_no_measurement_ingredient(self) -> bool:
        return len(self.no_measurement_ingredients) > 0

    @property
    def no_category_ingredients(self) -> list:
        return [i for i in self.ingredients if i.without_category]

    @property
    def has_no_category_ingredient(self) -> bool:
        return len(self.no_category_ingredients) > 0

    @property
    def without_category(self) -> bool:
        if self.is_shopping:
            return False

        return self.category is None or self.category.name == "---"

    @property
    def concat_ingredients(self) -> str:
        return ", ".join(o.name for o in self.ingredients)

    def has_label(self, label) -> bool:
        return label in self.labels

    def has_labels(self, labels) -> bool:
        return all(self.has_label(label) for label in labels)

    def has_any_of_labels(self, labels) -> bool:
        return any(self.has_label(label) for label in labels)

    @property
    def has_image(self) -> bool:
        return bool(self.images)

    @property
    def main_image(self):
        if not self.images:
            return None

        if main := [i for i in self.images if i.is_main]:
            return main[0]

        return self.images[0]

    @property
    def slugified_name(self) -> str:
        from app.helpers.general import slugify

        return slugify(self.name)

    @hybrid_property
    def reaction_count(self) -> int:
        return self.reactions.count()

    @reaction_count.expression
    def reaction_count(cls):
        from app.models import UserHasRecipeReaction
        from sqlalchemy import func, select

        return (
            select(func.count(UserHasRecipeReaction.recipe_id))
            .where(UserHasRecipeReaction.recipe_id == cls.id)
            .label("reaction_count")
        )

    @hybrid_property
    def author_name(self) -> str:
        return self.author.name

    @author_name.expression
    def author_name(cls):
        from app.models import User
        from sqlalchemy import select

        return select(User.full_name).where(User.id == cls.created_by)
