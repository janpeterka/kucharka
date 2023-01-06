from app.components import BaseComponent


class ButtonTo(BaseComponent):
    folder = "buttons"
    file = "button_to"

    def __init__(self, path, value, **kwargs):
        super(ButtonTo, self).__init__(**kwargs)
        self.path = path
        self.value = value
        self.kwargs["method"] = self.kwargs.pop("method", "POST")


# helpers
def button_to(path, value, **kwargs):
    return ButtonTo(path, value, **kwargs).render()


def icon_button_to(path, value, **kwargs):
    kwargs["class"] = f"fabutton text-primary ms-1 {kwargs.pop('class','')}"
    kwargs["form_class"] = f"d-inline-block {kwargs.pop('form_class','')}"

    return ButtonTo(path, value, **kwargs).render()
