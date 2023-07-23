from .. import BaseComponent


class Link(BaseComponent):
    def __init__(self, path, value, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.value = value
