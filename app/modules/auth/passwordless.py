import requests
import json
from flask import jsonify, request, Blueprint, redirect, url_for
from flask import current_app as app
from flask_security import current_user, login_user

passwordless = Blueprint("passwordless", __name__)


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
        json=payload,
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

        if body.get("success"):
            login_user(User.load(body["userId"]))
            return redirect(url_for("IndexView:index"))
        else:
            return jsonify(body)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
