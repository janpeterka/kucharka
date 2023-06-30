from app.components import BaseComponent


class Image(BaseComponent):
    def __init__(self, image, **kwargs):
        super(Image, self).__init__(**kwargs)
        self.src = image.url
        self.alt = image.full_name
        self.image = image


def recipe_gallery_image(image, editable=False, outer_class=None, **kwargs):
    # {% set class = kwargs.pop('class', "") %}
    # {% set style = kwargs.pop('style', "") %}
    # {% set thumbnail = kwargs.pop('thumbnail', False) %}
    # {% set with_delete = kwargs.pop('with_delete', False) %}
    # {% set with_pin = kwargs.pop('with_pin', False) %}
    # {% set center = kwargs.pop('center', False) %}

    # {% if thumbnail %}
    #     {% set url = image.thumbnail_url %}
    # {% else %}
    #     {% set url = image.url %}
    # {% endif %}

    if outer_class is None:
        outer_class = "pos-r"
    else:
        outer_class += " pos-r"

    if kwargs.pop("center", False):
        outer_class += " t-y--50"

    return Image(image, outer_class=outer_class, **kwargs).render()
