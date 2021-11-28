from .files import FilesView

__all__ = ["FilesView"]


def register_all_controllers(application):
    FilesView.register(application)
