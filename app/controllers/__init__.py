from .dashboard import DashboardView
from .daily_plans import DailyPlanView
from .daily_plan_recipes import DailyPlanRecipeView
from .event_exporter import EventExporterView

from .events.events import EventView
from .events.share_events import ShareEventView
from .events.published_events import PublishedEventView

from .errors import ErrorView
from .index import IndexView
from .support import SupportView

from .ingredients import IngredientView
from .fast_add_ingredients import FastAddIngredientView

from .ingredient_categories import IngredientCategorieView
from .recipe_categories import RecipeCategorieView
from .measurements import MeasurementView
from .conversions import ConversionView
from .tips import TipView
from .admin import AdminView

from .recipes import RecipeView
from .edit_recipes import EditRecipeView
from .edit_recipe_ingredients import EditRecipeIngredientView
from .public_recipes import PublicRecipeView
from .public_ingredients import PublicIngredientView

from .users import UserView
from .user_calendars import UserCalendarView

from .files import FileView


__all__ = [
    "DashboardView",
    "DailyPlanView",
    "DailyPlanRecipeView",
    "EventExporterView",
    "EventView",
    "ShareEventView",
    "PublishedEventView",
    "ErrorView",
    "IndexView",
    "SupportView",
    "IngredientView",
    "FastAddIngredientView",
    "IngredientCategorieView",
    "RecipeCategorieView",
    "MeasurementView",
    "ConversionView",
    "TipView",
    "AdminView",
    "RecipeView",
    "EditRecipeView",
    "EditRecipeIngredientView",
    "PublicRecipeView",
    "PublicIngredientView",
    "UserView",
    "UserCalendarView",
    "FileView",
]


def register_all_controllers(application):
    from app.helpers.helper_flask_view import HelperFlaskView

    DailyPlanView.register(application, base_class=HelperFlaskView)
    DailyPlanRecipeView.register(application, base_class=HelperFlaskView)

    DashboardView.register(application, base_class=HelperFlaskView)

    EventView.register(application, base_class=HelperFlaskView)
    ShareEventView.register(application, base_class=HelperFlaskView)
    PublishedEventView.register(application, base_class=HelperFlaskView)

    EventExporterView.register(application, base_class=HelperFlaskView)

    ErrorView.register(application)
    SupportView.register(application)

    IndexView.register(application)

    IngredientView.register(application, base_class=HelperFlaskView)
    FastAddIngredientView.register(application)
    PublicIngredientView.register(application, base_class=HelperFlaskView)

    IngredientCategorieView.register(application, base_class=HelperFlaskView)

    MeasurementView.register(application, base_class=HelperFlaskView)
    ConversionView.register(application, base_class=HelperFlaskView)

    TipView.register(application, base_class=HelperFlaskView)
    AdminView.register(application, base_class=HelperFlaskView)

    RecipeCategorieView.register(application, base_class=HelperFlaskView)

    RecipeView.register(application, base_class=HelperFlaskView)
    EditRecipeView.register(application, base_class=HelperFlaskView)
    EditRecipeIngredientView.register(application, base_class=HelperFlaskView)
    PublicRecipeView.register(application, base_class=HelperFlaskView)

    UserView.register(application, base_class=HelperFlaskView)
    UserCalendarView.register(application, base_class=HelperFlaskView)

    FileView.register(application, base_class=HelperFlaskView)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
