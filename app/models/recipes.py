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

    recipe_ingredients = db.relationship("RecipeHasIngredient", back_populates="recipe")

    ingredients = db.relationship(
        "Ingredient",
        primaryjoin="and_(Recipe.id == remote(RecipeHasIngredient.recipe_id), foreign(Ingredient.id) == RecipeHasIngredient.ingredient_id)",
        viewonly=True,
        order_by="Ingredient.name",
    )

    author = db.relationship("User", uselist=False, backref="recipes")

    @staticmethod
    def load(recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe is None:
            return None

        print(recipe.ingredients)

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

    @property
    def concat_ingredients(self) -> str:
        return ", ".join([o.name for o in self.ingredients])

    # PERMISSIONS

    @property
    def can_current_user_show(self) -> bool:
        return current_user == self.author or current_user.is_admin or self.public
