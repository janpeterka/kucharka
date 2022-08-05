from .attendees import AttendeeView
from .attendance import AttendanceView
from .dashboard import DashboardView
from .daily_plans import DailyPlanView
from .daily_plan_tasks import DailyPlanTaskView
from .daily_plan_recipes import DailyPlanRecipeView
from .event_exporter import EventExporterView
from .exports.event_cookbook_exporter import EventCookbookExporterView
from .exports.event_timetable_exporter import EventTimetableExporterView


from .events.events import EventView
from .events.share_events import ShareEventView
from .events.published_events import PublishedEventView
from .event_portion_types import EventPortionTypeView

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
from .recipe_tasks import RecipeTaskView
from .edit_recipes import EditRecipeView
from .edit_recipe_ingredients import EditRecipeIngredientView
from .public_recipes import PublicRecipeView
from .public_ingredients import PublicIngredientView

from .users import UserView
from .user_calendars import UserCalendarView

from .files import FileView

from .portion_types import PortionTypeView

__all__ = [
    "AttendeeView",
    "AttendanceView",
    "DashboardView",
    "DailyPlanView",
    "DailyPlanTaskView",
    "DailyPlanRecipeView",
    "EventExporterView",
    "EventView",
    "EventCookbookExporterView",
    "EventTimetableExporterView",
    "EventPortionTypeView",
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
    "RecipeTaskView",
    "EditRecipeView",
    "EditRecipeIngredientView",
    "PublicRecipeView",
    "PublicIngredientView",
    "UserView",
    "UserCalendarView",
    "FileView",
    "PortionTypeView",
]


def register_all_controllers(application):
    from app.helpers.helper_flask_view import HelperFlaskView

    AttendeeView.register(application, base_class=HelperFlaskView)
    AttendanceView.register(application, base_class=HelperFlaskView)

    DailyPlanView.register(application, base_class=HelperFlaskView)
    DailyPlanTaskView.register(application, base_class=HelperFlaskView)
    DailyPlanRecipeView.register(application, base_class=HelperFlaskView)

    DashboardView.register(application, base_class=HelperFlaskView)

    EventView.register(application, base_class=HelperFlaskView)
    ShareEventView.register(application, base_class=HelperFlaskView)
    PublishedEventView.register(application, base_class=HelperFlaskView)
    EventPortionTypeView.register(application, base_class=HelperFlaskView)

    EventExporterView.register(application, base_class=HelperFlaskView)
    EventCookbookExporterView.register(application, base_class=HelperFlaskView)
    EventTimetableExporterView.register(application, base_class=HelperFlaskView)

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
    RecipeTaskView.register(application, base_class=HelperFlaskView)
    EditRecipeView.register(application, base_class=HelperFlaskView)
    EditRecipeIngredientView.register(application, base_class=HelperFlaskView)
    PublicRecipeView.register(application, base_class=HelperFlaskView)

    UserView.register(application, base_class=HelperFlaskView)
    UserCalendarView.register(application, base_class=HelperFlaskView)

    FileView.register(application, base_class=HelperFlaskView)

    PortionTypeView.register(application, base_class=HelperFlaskView)


def register_error_handlers(application):
    from .errors import error404
    from .errors import error405
    from .errors import error500

    application.register_error_handler(403, error404)
    application.register_error_handler(404, error404)
    application.register_error_handler(405, error405)
    application.register_error_handler(500, error500)
