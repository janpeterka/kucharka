from .dashboard import DashboardView
from .daily_plans import DailyPlansView
from .daily_plans_edit import DailyPlansEditView
from .event_exporter import EventExporterView

from .events.events import EventsView
from .events.edit_events import EditEventView

from .errors import ErrorsView
from .index import IndexView
from .support import SupportView

from .ingredients import IngredientsView
from .fast_add_ingredients import FastAddIngredientsView

from .ingredient_categories import IngredientCategoriesView
from .recipe_categories import RecipeCategoriesView
from .measurements import MeasurementsView
from .conversions import ConversionsView
from .tips import TipsView
from .admin import AdminView

from .recipes import RecipesView
from .edit_recipes import EditRecipeView
from .public_recipes import PublicRecipesView
from .public_ingredients import PublicIngredientsView

from .users import UsersView
from .user_statistics import UserStatisticsView
from .user_calendars import UserCalendarsView

from .files import FilesView


__all__ = [
    "DashboardView",
    "DailyPlansView",
    "DailyPlansEditView",
    "EventExporterView",
    "EventsView",
    "EditEventView",
    "ErrorsView",
    "IndexView",
    "SupportView",
    "IngredientsView",
    "FastAddIngredientsView",
    "IngredientCategoriesView",
    "RecipeCategoriesView",
    "MeasurementsView",
    "ConversionsView",
    "TipsView",
    "AdminView",
    "RecipesView",
    "EditRecipeView",
    "PublicRecipesView",
    "PublicIngredientsView",
    "UsersView",
    "UserStatisticsView",
    "UserCalendarsView",
    "FilesView",
]


def register_all_controllers(application):
    from app.helpers.helper_flask_view import HelperFlaskView

    DailyPlansView.register(application, base_class=HelperFlaskView)
    DailyPlansEditView.register(application, base_class=HelperFlaskView)

    DashboardView.register(application, base_class=HelperFlaskView)

    EventsView.register(application, base_class=HelperFlaskView)
    EditEventView.register(application, base_class=HelperFlaskView)

    EventExporterView.register(application, base_class=HelperFlaskView)

    ErrorsView.register(application)
    SupportView.register(application)

    IndexView.register(application)

    IngredientsView.register(application, base_class=HelperFlaskView)
    FastAddIngredientsView.register(application)
    PublicIngredientsView.register(application, base_class=HelperFlaskView)

    IngredientCategoriesView.register(application, base_class=HelperFlaskView)

    MeasurementsView.register(application, base_class=HelperFlaskView)
    ConversionsView.register(application, base_class=HelperFlaskView)

    TipsView.register(application, base_class=HelperFlaskView)
    AdminView.register(application, base_class=HelperFlaskView)

    RecipeCategoriesView.register(application, base_class=HelperFlaskView)

    RecipesView.register(application, base_class=HelperFlaskView)
    EditRecipeView.register(application, base_class=HelperFlaskView)
    PublicRecipesView.register(application, base_class=HelperFlaskView)

    UsersView.register(application, base_class=HelperFlaskView)
    UserStatisticsView.register(application, base_class=HelperFlaskView)
    UserCalendarsView.register(application, base_class=HelperFlaskView)

    FilesView.register(application, base_class=HelperFlaskView)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
