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
        *,
        icon_class=None,
        tooltip=None,
        cursor_class=None,
        color_class=None,
        **kwargs,
    ):
        self.kwargs = kwargs
        self.kwargs["tooltip"] = tooltip

        if cursor_class is None:
            cursor_class = self.DEFAULT_CURSOR_CLASS

        if icon_class is None and icon_alias:
            icon_class = self.ICON_CLASS_ALIASES.get(icon_alias, "")

        if color_class is None and icon_alias:
            color_class = self.ICON_ALIAS_COLORS.get(icon_alias)

        classes = kwargs.pop("class", "")

        kwargs["class"] = f"{classes} {color_class} {icon_class} {cursor_class}".strip()

    # @classmethod
    # def helpers(cls):
    #     def icon(alias, **kwargs):
    #         return cls(alias, **kwargs).render()

    #     return {"icon": icon}
