from app.presenters import ItemPresenter


class IngredientPresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "icon": "add",
            "value": "úkol",
            "button_type": "secondary-action",
        },
        "edit": {
            "icon": "edit",
            "value": "surovinu",
            "button_type": "secondary-action",
        },
        "delete": {
            "icon": "delete",
            "value": "surovinu",
            "button_type": "secondary-action",
        },
    }
