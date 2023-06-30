from app.presenters import ItemPresenter


class EventPresenter(ItemPresenter):
    LINK_INFO = {"new": {"value": "přidat akci"}}

    @property
    def duration_label(self) -> str:
        if self.duration == 1:
            return "den"
        elif self.duration in [1, 2, 3, 4]:
            return "dny"
        else:
            return "dní"

    @property
    def slugified_name(self) -> str:
        from app.helpers.general import slugify

        return slugify(self.name)

    @property
    def public_url(self):
        from app.helpers.general import obscure
        from flask import url_for

        if not self.is_shared:
            return None
        else:
            hash_value = obscure(str(self.id).encode())
            return url_for(
                "PublishedEventView:show", hash_value=hash_value, _external=True
            )
