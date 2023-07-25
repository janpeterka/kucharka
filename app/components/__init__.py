from .links import link_to, link_to_edit

# from .icons import icon
from .action_badges import action_badge
from .dropzone import dropzone
from .tables import table, search_box
from .images import recipe_gallery_image

# __all__ = ["icon"]

# from kucharka.packages.template_components.components import *


def register_all_components(application):
    # links
    application.add_template_global(link_to)
    application.add_template_global(link_to_edit)

    # icons
    from .icons import Icon

    Icon.register_helper(application)

    # application.add_template_global(icon, name="icon")

    # action badges
    application.add_template_global(action_badge)

    # dropzone
    application.add_template_global(dropzone)

    # tables
    application.add_template_global(table)
    application.add_template_global(search_box)

    # images
    application.add_template_global(recipe_gallery_image)
