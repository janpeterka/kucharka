from sqlalchemy.orm.exc import NoResultFound

from flask import Blueprint, redirect, request, url_for
from flask_security import login_user

from app import skautis, db
from app.models.oauth import OAuth
from app.models.users import User

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

    skautis_id = user_info["ID"]
    user_id = user_info["ID_Person"]

    user_info_external = skautis.UserManagement.UserDetailExternal(
        skautis_token, skautis_id, user_id
    )

    first_name = user_info_external["FirstName"]
    last_name = user_info_external["LastName"]
    full_name = f"{first_name} {last_name}"
    email = user_info_external["Email"]

    # Find this OAuth token in the database, or create it
    try:
        oauth = OAuth.query.filter_by(
            provider="skautis", provider_user_id=user_id
        ).one()
    except NoResultFound:
        oauth = OAuth(
            provider="skautis", provider_user_id=user_id, token={"token": skautis_token}
        )

    if oauth.user:
        login_user(oauth.user)
    else:
        # Try finding user with given e-mail in database
        user = User.load_by_attribute("email", email)
        if not user:
            # Create a new local user account for this user
            user = User.create(
                email=email,
                password="x",
                full_name=full_name,
                active=True,
                do_hash=False,
            )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)

    # Disable Flask-Dance's default behavior for saving the OAuth token

    return redirect(url_for("DashboardView:index"))
