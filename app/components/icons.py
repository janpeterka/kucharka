from kucharka.packages.template_components import BaseComponent


class Icon(BaseComponent):
    pass


def icon(name, **kwargs):
    icon_name = icon_group_to_icon.get(name, name)
    fa_class = kwargs.pop("fa_class", icon_fa_classes.get(icon_name, ""))
    color_class = kwargs.pop("color_class", icon_color_classes.get(icon_name, ""))
    classes = f"{kwargs.pop('class', '')} {kwargs.pop('class_', '')}"

    kwargs["cursor_class"] = kwargs.pop("cursor_class", "cursor-default")

    kwargs[
        "class"
    ] = f"{classes} {color_class} {fa_class} {kwargs['cursor_class']}".strip()

    kwargs["tooltip"] = kwargs.pop("tooltip", None)

    return Icon(**kwargs).render()


icon_group_to_icon = {}

icon_fa_classes = {
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

default_tooltips = {
    "shared": "zveřejněno",
    "public": "z veřejných",
    "collaborator": "editace",
    "viewer": "prohlížení",
}

icon_color_classes = {
    # "completed": "text-success",
    # "question-mark": "text-muted",
}
