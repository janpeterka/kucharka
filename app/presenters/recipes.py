from app.presenters import ItemPresenter


class RecipePresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "name": "recept",
            "value": "recept",
        }
    }
