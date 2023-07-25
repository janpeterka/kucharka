from .. import BaseComponent


class BaseIcon(BaseComponent):
    DEFAULT_CURSOR_CLASS = "cursor-default"
    ICON_CLASS_ALIASES = {}
    ICON_ALIAS_COLORS = {}
    folder = "icons"
    file = "icon"

    def __init__(
        self,
        icon_alias=None,
        *args,
        icon_class=None,
        tooltip=None,
        cursor_class=None,
        color_class=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.kwargs["tooltip"] = tooltip

        icon_class_aliases = self.kwargs.pop(
            "icon_class_aliases", self.ICON_CLASS_ALIASES
        )
        icon_alias_colors = self.kwargs.pop("icon_alias_colors", self.ICON_ALIAS_COLORS)

        if "ICON_ALIAS_COLORS" in self.kwargs:
            self.ICON_ALIAS_COLORS = self.kwargs.pop("ICON_ALIAS_COLORS")

        if cursor_class is None:
            cursor_class = self.DEFAULT_CURSOR_CLASS

        if icon_class is None and icon_alias:
            icon_class = icon_class_aliases.get(icon_alias, "")

        if color_class is None and icon_alias:
            color_class = icon_alias_colors.get(icon_alias, "")

        self.css_classes.append(color_class)
        self.css_classes.append(icon_class)
        self.css_classes.append(cursor_class)
