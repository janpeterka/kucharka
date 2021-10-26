from unidecode import unidecode

from flask_security import current_user

from app import db, BaseModel

from app.helpers.item_mixin import ItemMixin
from app.helpers.general import list_without_duplicated

from app.models.ingredients import Ingredient
from app.models.recipes_have_ingredients import RecipeHasIngredient
from app.models.label_categories import LabelCategory

from app.models.mixins.recipes.recipe_reactions import RecipeReactionMixin
from app.models.mixins.recipes.recipe_ingredients import RecipeIngredientMixin


class Recipe(BaseModel, ItemMixin, RecipeReactionMixin, RecipeIngredientMixin):
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
        primaryjoin="Recipe.id == DailyPlanHasRecipe.recipe_id",
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
        return Recipe.query.filter(
            Recipe.ingredients.any(Ingredient.id == ingredient.id)
        ).all()

    @staticmethod
    def load_by_ingredient_and_user(ingredient, user):
        recipes = Recipe.load_by_ingredient(ingredient)
        return [r for r in recipes if r.author == user]

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

        new.name = self.name
        new.author = current_user
        new.description = self.description
        new.portion_count = self.portion_count
        new.category = self.category
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
    def can_current_user_view(self) -> bool:
        return (
            self.is_shared
            or self.is_in_shared_event
            or current_user == self.author
            or current_user.is_admin
        )

    # PROPERTIES

    @property
    def is_shopping(self) -> bool:
        return self.author.is_admin and self.name == "Nákup"

    @property
    def is_used(self) -> bool:
        return bool(self.daily_plans)

    @property
    def is_visible(self) -> bool:
        return not self.is_draft

    @property
    def events(self):
        events = [dp.event for dp in self.daily_plans]
        return list_without_duplicated(events)

    @property
    def shared_events(self):
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
