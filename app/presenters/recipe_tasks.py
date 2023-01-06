from app.presenters import ItemPresenter
from app.helpers.general import classproperty


class RecipeTaskPresenter(ItemPresenter):
    @classproperty
    def link_info(cls):
        return {
            "new": {
                "icon": "add",
                "value": "úkol",
                "button_type": "secondary-action",
            }
        }
