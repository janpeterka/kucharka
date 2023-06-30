from app.presenters import ItemPresenter


class RecipeTaskPresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "icon": "add",
            "value": "úkol",
            "button_type": "secondary-action",
        }
    }
