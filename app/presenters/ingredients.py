from app.presenters import ItemPresenter


class IngredientPresenter(ItemPresenter):
    LINK_INFO = {
        "new": {
            "value": "přidat surovinu",
        },
        "edit": {
            "value": "upravit",
        },
        "delete": {
            "value": "smazat surovinu",
            "confirmation": "určitě chceš smazat surovinu? už to nepůjde vrátit!",
        },
    }
