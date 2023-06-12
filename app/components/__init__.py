from .base import BaseComponent
from .links import link_to, link_to_edit
from .icons import icon
from .action_badges import action_badge
from .dropzone import dropzone


__all__ = ["icon", "BaseComponent"]


def register_all_components(application):
    # links
    application.add_template_global(link_to)
    application.add_template_global(link_to_edit)

    # icons
    application.add_template_global(icon)

    # action badges
    application.add_template_global(action_badge)

    # dropzone
    application.add_template_global(dropzone)
