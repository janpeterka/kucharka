from .dashboard import DashboardView
from .daily_plans import DailyPlansView
from .event_exporter import EventExporterView

from .events import EventsView
from .edit_events import EditEventView

from .errors import ErrorsView
from .index import IndexView

from .ingredients import IngredientsView
from .fast_add_ingredients import FastAddIngredientsView

from .ingredient_categories import IngredientCategoriesView
from .recipe_categories import RecipeCategoriesView
from .measurements import MeasurementsView

from .recipes import RecipesView
from .edit_recipes import EditRecipeView
from .public_recipes import PublicRecipesView

from .users import UsersView

__all__ = [
    "DashboardView",
    "DailyPlansView",
    "EventExporterView",
    "EventsView",
    "EditEventView",
    "ErrorsView",
    "IndexView",
    "IngredientsView",
    "FastAddIngredientsView",
    "IngredientCategoriesView",
    "MeasurementsView",
    "RecipeCategoriesView",
    "RecipesView",
    "EditRecipeView",
    "PublicRecipesView",
    "UsersView",
]


def register_all_controllers(application):
    DailyPlansView.register(application)

    DashboardView.register(application)

    EventsView.register(application)
    EditEventView.register(application)

    EventExporterView.register(application)

    ErrorsView.register(application)

    IndexView.register(application)

    IngredientsView.register(application)
    FastAddIngredientsView.register(application)

    IngredientCategoriesView.register(application)

    MeasurementsView.register(application)

    RecipeCategoriesView.register(application)

    RecipesView.register(application)
    EditRecipeView.register(application)
    PublicRecipesView.register(application)

    UsersView.register(application)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
