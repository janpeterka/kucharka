from flask import Blueprint, redirect, request, url_for

from app import skautis

skautis_blueprint = Blueprint("skautis", __name__)


@skautis_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect(skautis.get_login_url())
    skautis_token = request.form["skautIS_Token"]
    # skautis_idrole = request.form["skautIS_IDRole"]
    # skautis_idunit = request.form["skautIS_IDUnit"]
    # skautis_datelogout = request.form["skautIS_DateLogout"]

    user_info = skautis.UserManagement.UserDetail(skautis_token, None)

    return redirect(url_for("DashboardView:dashboard"))
