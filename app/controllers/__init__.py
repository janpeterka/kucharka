from .dashboard import DashboardView
from .daily_plans import DailyPlansView
from .daily_plan_exporter import DailyPlanExporterView
from .events import EventsView
from .index import IndexView
from .ingredients import IngredientsView
from .ingredient_categories import IngredientCategoriesView
from .recipe_categories import RecipeCategoriesView
from .measurements import MeasurementsView
from .recipes import RecipesView
from .public_recipes import PublicRecipesView

__all__ = [
    "DashboardView",
    "DailyPlansView",
    "DailyPlanExporterView",
    "EventsView",
    "IndexView",
    "IngredientsView",
    "IngredientCategoriesView",
    "MeasurementsView",
    "RecipeCategoriesView",
    "RecipesView",
    "PublicRecipesView",
    # "UsersView",
]


def register_all_controllers(application):
    # AdminView.register(application)
    # CookbookView.register(application)
    DailyPlansView.register(application)
    DailyPlanExporterView.register(application)
    DashboardView.register(application)
    EventsView.register(application)
    # ErrorsView.register(application)
    # FilesView.register(application)
    IndexView.register(application)
    IngredientsView.register(application)
    IngredientCategoriesView.register(application)
    MeasurementsView.register(application)
    RecipeCategoriesView.register(application)
    RecipesView.register(application)
    PublicRecipesView.register(application)
    # SupportView.register(application)
    # UsersView.register(application)


# def register_error_handlers(application):
#     from .errors import error404
#     from .errors import error405
#     from .errors import error500

#     application.register_error_handler(403, error404)
#     application.register_error_handler(404, error404)
#     application.register_error_handler(405, error405)
#     application.register_error_handler(500, error500)
