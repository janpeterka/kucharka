# This is needed for ExtendedFlaskView to automatically import all Form classes

from .ingredients import IngredientsForm  # noqa: F401
from .events import EventsForm  # noqa: F401
from .recipes import RecipesForm  # noqa: F401
from .users import UsersForm  # noqa: F401
from .users import PasswordForm  # noqa: F401

__all__ = ["IngredientsForm", "EventsForm", "RecipesForm", "UsersForm", "PasswordForm"]
