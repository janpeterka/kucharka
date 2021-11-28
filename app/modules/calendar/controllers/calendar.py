#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, redirect
from flask import render_template as template

from flask_classful import route
from flask_security import permissions_required

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash

calendar_blueprint = Blueprint(
    "calendar", __name__, url_prefix="/calendar", template_folder="templates"
)


class CalendarView(HelperFlaskView):
    def show(self, user_hash):
        pass
