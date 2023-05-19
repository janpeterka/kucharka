import requests
import json
from flask import jsonify, request, Blueprint, redirect, url_for, flash
from flask import current_app as app
from flask_security import current_user, login_user
from app import security

passwordless = Blueprint("passwordless", __name__)


@passwordless.route("register-user", methods=["POST"])
def register_user():
    from app.models import User

    email = request.args.get("username")

    user = User.load_by(email=email)
    if user is not None:
        flash("Uživatel s tímto emailem již existuje", "warning")
        return redirect(url_for("SupportView:passwordless"))

    user = security.datastore.create_user(username=email, email=email)
    user.save()

    headers = {
        "ApiSecret": app.config["PASSWORDLESS_SECRET"],
        "Content-Type": "application/json",
    }

    payload = {"userId": user.id, "username": user.email}

    from sentry_sdk import capture_message

    capture_message(f"Registering user {user.id} {user.email}", level="info")

    response = requests.post(
        f"{app.config['PASSWORDLESS_URL']}/register/token",
        data=json.dumps(payload),
        headers=headers,
        timeout=5,
    )

    capture_message(
        f"response from passwordless is {response} ({response.__dict__})", level="info"
    )

    if response.ok:
        token = response.json().get("token")
        login_user(user)
        return jsonify({"token": token}), 200
    else:
        flash("ajaj, něco se nepovedlo", "error")
        return jsonify({"error": "not ok"}), 404


@passwordless.route("register-token")
def register_token():
    payload = {
        "userId": current_user.id,
        "username": current_user.email,
    }

    headers = {
        "ApiSecret": app.config["PASSWORDLESS_SECRET"],
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{app.config['PASSWORDLESS_URL']}/register/token",
        data=payload,
        headers=headers,
        timeout=5,
    )

    token = response.json().get("token")
    # Process the token or perform any additional logic here
    return {"token": token}


@passwordless.route("/signin", methods=["POST"])
def verify_sign_in():
    from app.models import User

    try:
        token = request.args.get("token")

        url = f"{app.config['PASSWORDLESS_URL']}/signin/verify"
        api_secret = app.config["PASSWORDLESS_SECRET"]
        headers = {"ApiSecret": api_secret, "Content-Type": "application/json"}
        json_data = json.dumps({"token": token})

        response = requests.post(url, data=json_data, headers=headers, timeout=5)
        body = response.json()

        if not body.get("success"):
            flash("ajaj, něco se nepovedlo", "error")
            return jsonify(body)

        login_user(User.load(body["userId"]))
        return redirect(url_for("IndexView:index"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
