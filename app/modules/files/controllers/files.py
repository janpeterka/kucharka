#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, redirect
from flask import render_template as template

from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash

from ..models.files import File
from ..handlers.files import FileHandler

files_blueprint = Blueprint(
    "files", __name__, url_prefix="/files", template_folder="templates"
)


class FilesView(HelperFlaskView):
    def show(self, hash_value):
        file = File.load_first_by_attribute("hash", hash_value)
        thumbnail = request.args.get("thumbnail", False) == "True"

        # if not file:
        #     abort(404)
        # if not file.can_current_user_view:
        #     abort(403)
        self.validate_operation(file, hash_value)

        return FileHandler().show(file, thumbnail=thumbnail)

    @route("/<id>/delete", methods=["POST"])
    def delete(self, id):
        file = File.load(id)
        if self.validate_edit(file):
            file.delete()
        else:
            flash("Nemáte právo toto foto smazat.", "error")

        return redirect(request.referrer)

    # def show_profile_pic(self, user_id):
    #     from app.models.users import User
    #     file = User.load(user_id).profile_picture_file
    #     if not file:
    #         return FileHandler().show_new_user_placeholder()
    #     if not file.can_view(current_user):
    #         abort(403)
    #     return FileHandler().show(file)

    def download(self, id):
        file = File.load(id)
        self.validate_operation(file, id)

        return FileHandler().download(file)

    def index(self):
        return template("files/index.html.j2", files=FileHandler().all_files)
