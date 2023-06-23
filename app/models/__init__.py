from .attendees import Attendee
from .attendees_have_labels import AttendeeHasLabel
from .conversions import Conversion
from .daily_plans import DailyPlan
from .daily_plan_tasks import DailyPlanTask
from .daily_plans_have_recipes import DailyPlanRecipe
from .events import Event
from .event_portion_types import EventPortionType
from .files import File, RecipeImageFile
from .ingredient_categories import IngredientCategory
from .ingredients import Ingredient
from .label_categories import LabelCategory
from .labels import Label
from .measurements import Measurement
from .oauth import OAuth
from .portion_types import PortionType
from .recipe_tasks import RecipeTask
from .recipes import Recipe
from .recipe_categories import RecipeCategory
from .recipes_have_ingredients import RecipeHasIngredient
from .recipes_have_labels import RecipeHasLabel
from .request_logs import RequestLog
from .roles import Role
from .tips import Tip
from .users import User
from .users_have_event_roles import UserHasEventRole
from .users_have_recipes_reaction import UserHasRecipeReaction
from .users_have_roles import users_have_roles  # noqa: F401

# non-db models
from .event_days import EventDay


__all__ = [
    "Attendee",
    "AttendeeHasLabel",
    "Conversion",
    "DailyPlan",
    "DailyPlanTask",
    "DailyPlanRecipe",
    "Event",
    "EventPortionType",
    "File",
    "Ingredient",
    "IngredientCategory",
    "Label",
    "LabelCategory",
    "Measurement",
    "OAuth",
    "PortionType",
    "Recipe",
    "RecipeHasIngredient",
    "RecipeHasLabel",
    "RecipeImageFile",
    "RecipeTask",
    "RecipeCategory",
    "RequestLog",
    "Role",
    "Tip",
    "User",
    "UserHasEventRole",
    "UserHasRecipeReaction",
    # non-db models
    "EventDay",
]

models_dictionary = {
    "Attendee": Attendee,
    "Conversion": Conversion,
    "DailyPlan": DailyPlan,
    "DailyPlanTask": DailyPlanTask,
    "DailyPlanRecipe": DailyPlanRecipe,
    "Event": Event,
    "EventPortionType": EventPortionType,
    "File": File,
    "Ingredient": Ingredient,
    "IngredientCategory": IngredientCategory,
    "Label": Label,
    "LabelCategory": LabelCategory,
    "Measurement": Measurement,
    "PortionType": PortionType,
    "Recipe": Recipe,
    "RecipeImageFile": RecipeImageFile,
    "RecipeTask": RecipeTask,
    "RecipeCategory": RecipeCategory,
    "Role": Role,
    "Tip": Tip,
    "User": User,
}
