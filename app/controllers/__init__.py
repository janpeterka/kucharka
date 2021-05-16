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
from .public_ingredients import PublicIngredientsView

from .users import UsersView

from app.helpers.helper_flask_view import HelperFlaskView

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
    "PublicIngredientsView",
    "UsersView",
]


def register_all_controllers(application):
    DailyPlansView.register(application, base_class=HelperFlaskView)

    DashboardView.register(application, base_class=HelperFlaskView)

    EventsView.register(application, base_class=HelperFlaskView)
    EditEventView.register(application, base_class=HelperFlaskView)

    EventExporterView.register(application, base_class=HelperFlaskView)

    ErrorsView.register(application)

    IndexView.register(application)

    IngredientsView.register(application, base_class=HelperFlaskView)
    FastAddIngredientsView.register(application)
    PublicIngredientsView.register(application, base_class=HelperFlaskView)

    IngredientCategoriesView.register(application, base_class=HelperFlaskView)

    MeasurementsView.register(application, base_class=HelperFlaskView)

    RecipeCategoriesView.register(application, base_class=HelperFlaskView)

    RecipesView.register(application, base_class=HelperFlaskView)
    EditRecipeView.register(application, base_class=HelperFlaskView)
    PublicRecipesView.register(application, base_class=HelperFlaskView)

    UsersView.register(application)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
