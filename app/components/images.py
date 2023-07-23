from app.packages.template_components import BaseComponent


class Image(BaseComponent):
    def __init__(self, image, **kwargs):
        super(Image, self).__init__(**kwargs)
        if kwargs.get("thumbnail", False):
            self.src = image.thumbnail_url
        else:
            self.src = image.url

        self.alt = image.full_name
        self.image = image


def recipe_gallery_image(image, editable=False, outer_class=None, **kwargs):
    if outer_class is None:
        outer_class = "pos-r"
    else:
        outer_class += " pos-r"

    if kwargs.pop("center", False):
        outer_class += " t-y--50"

    return Image(image, outer_class=outer_class, **kwargs).render()
