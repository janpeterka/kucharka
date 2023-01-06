from app.presenters import ItemPresenter
from app.helpers.general import classproperty


class RecipePresenter(ItemPresenter):
    @classproperty
    def link_info(cls):
        from flask import url_for

        return {
            "new": {
                "name": "recept",
                "icon": "add",
                "path": url_for("RecipeView:new"),
                "value": "recept",
            }
        }
