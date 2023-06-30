from app.presenters import ItemPresenter


class IngredientPresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "value": "přidat surovinu",
        },
        "edit": {
            "value": "surovinu",
        },
        "delete": {
            "value": "surovinu",
        },
    }
