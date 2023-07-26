from .. import BaseComponent


class Image(BaseComponent):
    def __init__(self, src: str = None, alt: str = None, **kwargs):
        super().__init__(**kwargs)

        if src is not None:
            self.src = src

        if alt is not None:
            self.alt = alt


class ImageWithObject(Image):
    def __init__(
        self,
        src: str = None,
        alt: str = None,
        image: object = None,
        thumbnail: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)

        if src is not None:
            self.src = src
        elif thumbnail is not None and hasattr("image", "thumbnail_url"):
            self.src = image.thumbnail_url
        elif hasattr(image, "src"):
            self.src = image.src
        elif hasattr(image, "url"):
            self.src = image.url

        if alt is not None:
            self.alt = alt
        elif hasattr(image, "alt"):
            self.alt = image.alt
        elif hasattr(image, "name"):
            self.alt = image.name

        self.image = image
