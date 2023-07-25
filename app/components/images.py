from kucharka.packages.template_components.components import ImageWithObject


class Image(ImageWithObject):
    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)

        self.alt = image.full_name


class RecipeGalleryImage(Image):
    def __init__(self, image, editable=False, outer_class=None, **kwargs):
        super().__init__(**kwargs)

        self.alt = image.full_name


def recipe_gallery_image(image, editable=False, outer_class=None, **kwargs):
    if outer_class is None:
        outer_class = "pos-r"
    else:
        outer_class += " pos-r"

    if kwargs.pop("center", False):
        outer_class += " t-y--50"

    return Image(image, outer_class=outer_class, **kwargs).render()
