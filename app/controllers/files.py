from flask import request, redirect
from flask import render_template as template

from flask_classful import route
from flask_security import permissions_required

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash

from app.models.files import File

from app.modules.files import show_file, download_file, all_files


class FilesView(HelperFlaskView):
    @permissions_required("manage-application")
    def index(self):
        return template("files/index.html.j2", files=all_files())

    def show(self, hash_value):
        file = File.load_by_attribute("hash", hash_value)
        thumbnail = request.args.get("thumbnail", False) == "True"

        self.validate_show(file)

        return show_file(file, thumbnail)

    @route("/<id>/delete", methods=["POST"])
    def delete(self, id):
        file = File.load(id)
        if self.validate_edit(file):
            file.delete()
        else:
            flash("Nemáte právo toto foto smazat.", "error")

        return redirect(request.referrer)

    def download(self, id):
        file = File.load(id)
        self.validate_show(file)

        return download_file(file)
