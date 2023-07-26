from flask_template_components.components import ImageWithObject


class Image(ImageWithObject):
    def __init__(self, image, **kwargs):
        super().__init__(image=image, **kwargs)

        self.alt = image.full_name


class RecipeGalleryImage(Image):
    DEFAULT_CLASSES = ["img-fluid"]

    def __init__(self, image, editable=False, outer_class=None, center=False, **kwargs):
        super().__init__(image=image, **kwargs)

        if outer_class:
            self.outer_class = outer_class
        else:
            self.outer_class = ""

        self.outer_class += " pos-r"

        if center:
            self.outer_class += " t-y--50"


def recipe_gallery_image(image, editable=False, outer_class=None, **kwargs):
    return RecipeGalleryImage(image, outer_class=outer_class, **kwargs).render()
