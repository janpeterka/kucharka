from flask import flash
from flask_security import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.users import User
from app.models.oauth import OAuth


blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    response = blueprint.session.get("/oauth2/v1/userinfo")
    if not response.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = response.json()
    user_id = info["id"]
    first_name = info.get("given_name", None)
    last_name = info.get("family_name", None)
    if first_name and last_name:
        full_name = f"{first_name} {last_name}"
    else:
        full_name = None

    # Find this OAuth token in the database, or create it
    try:
        oauth = OAuth.query.filter_by(
            provider=blueprint.name, provider_user_id=user_id
        ).one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
    else:
        # Try finding user with given e-mail in database
        user = User.load_by_attribute("email", info["email"])
        if not user:
            # Create a new local user account for this user
            user = User.create(
                email=info["email"],
                password=_generate_password(),
                full_name=full_name,
                active=True,
            )
        # user.save()
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # oauth.save()
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


def _generate_password():
    import secrets
    import string

    alphabet = string.ascii_letters + string.digits
    return "".join(
        secrets.choice(alphabet) for i in range(80)
    )
