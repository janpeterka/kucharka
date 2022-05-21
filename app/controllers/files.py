from flask import request, redirect
from flask import render_template as template

from flask_classful import route
from flask_security import permissions_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.files import File

from app.modules.files import show_file, download_file, all_files


class FileView(HelperFlaskView):
    def before_show(self, hash_value):
        self.file = File.load_by_attribute("hash", hash_value)
        self.validate_show(self.file)

    def before_delete(self, id):
        self.file = File.load(id)
        self.validate_delete(self.file)

    def before_download(self, id):
        self.file = File.load(id)
        self.validate_show(self.file)

    @permissions_required("manage-application")
    def index(self):
        return template("files/index.html.j2", files=all_files())

    def show(self, hash_value):
        thumbnail = request.args.get("thumbnail", False) == "True"

        return show_file(self.file, thumbnail)

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        self.file.delete()

        return redirect(request.referrer)

    def download(self, id):
        return download_file(self.file)
