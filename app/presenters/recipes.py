from app.presenters import ItemPresenter


class RecipePresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "name": "recept",
            "value": "přidat recept",
        },
        "edit": {
            "value": "upravit recept",
        },
        "duplicate": {
            "name": "recept",
            "value": "zkopírovat do mých receptů",
            "icon": "duplicate",
        },
    }
