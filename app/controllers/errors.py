from flask import abort, make_response
from flask import render_template as template

from flask_security import permissions_required
from flask_classful import FlaskView


class ErrorsView(FlaskView):
    def wrongpage(self):
        abort(405)

    def shutdown(self):
        return template("errors/shutdown.html.j2")

    # only for testing
    @permissions_required("see-debug")
    def err404(self):
        return template("errors/err404.html.j2")

    # only for testing
    @permissions_required("see-debug")
    def err405(self):
        return template("errors/err405.html.j2")

    # only for testing
    @permissions_required("see-debug")
    def err500(self):
        return template("errors/err500.html.j2")


def error404(error):
    # Missing page
    return template("errors/err404.html.j2"), 404


def error405(error=None):
    # Action not allowed
    return make_response(template("errors/err405.html.j2"), 405)


def error500(error):
    # Internal error
    return make_response(template("errors/err500.html.j2"), 500)
