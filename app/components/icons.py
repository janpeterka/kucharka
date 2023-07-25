from kucharka.packages.template_components.components import BaseIcon


class Icon(BaseIcon):
    ICON_CLASS_ALIASES = {
        "user": "far fa-user-circle",
        "daily": "fas fa-calendar-alt",
        "more": "fas fa-ellipsis-h",
        "image": "far fa-image",
        # operations
        "add": "fas fa-plus",
        "edit": "fas fa-pencil-alt",
        "delete": "fas fa-trash",
        "remove": "fas fa-times",
        "duplicate": "far fa-clone",
        "archive": "fas fa-archive",
        "archived": "fas fa-archive",
        "unarchive": "fas fa-archive",
        "previous": "fas fa-chevron-left",
        "next": "fas fa-chevron-right",
        "clipboard": "fa fa-clipboard",
        # sharing, publishing,...
        "shared": "fas fa-user-friends",
        "share": "fas fa-user-friends",
        "unshare": "fas fa-ban",
        "public": "fas fa-user-friends",
        "heart_empty": "far fa-heart color-highlight",
        "heart_full": "fas fa-heart color-highlight",
        "person": "fa fa-user",
        "collaborator": "fas fa-user-edit",
        "viewer": "far fa-eye",
        # misc
        "recipe_database": "fas fa-book-open",
        "cookbook": "fas fa-book",
        "food": "fas fa-utensils",
        "shopping": "fas fa-shopping-basket",
        "info": "fas fa-info",
        "info-circle": "fas fa-info-circle",
        "list": "fas fa-list-ul",
        "seedling": "fas fa-seedling",
        "up": "fas fa-sort-up",
        "down": "fas fa-sort-down",
        "check": "fa fa-check",
        # brands
        "github": "fab fa-github",
        "facebook": "fab fa-facebook-square",
        "pdf": "fas fa-file-pdf",
        # navbar
        "nav-home": "fas fa-home",
        "nav-public-recipes": "fas fa-book-open",
        "nav-profile": "fa fa-user",
        "nav-logout": "fas fa-sign-out-alt",
    }


def icon(name, **kwargs):
    return Icon(name, **kwargs).render()


# default_tooltips = {
#     "shared": "zveřejněno",
#     "public": "z veřejných",
#     "collaborator": "editace",
#     "viewer": "prohlížení",
# }
