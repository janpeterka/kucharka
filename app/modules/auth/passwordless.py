import requests
from flask import jsonify, request, Blueprint
from flask import current_app as app
from flask_security import current_user

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
    import json
    from sentry_sdk import capture_message

    try:
        token = request.args.get("token")

        api_secret = app.config["PASSWORDLESS_SECRET"]
        headers = {"ApiSecret": api_secret, "Content-Type": "application/json"}
        json = json.dumps({"token": token})
        capture_message("This is going fine")

        response = requests.post(
            "https://v4.passwordless.dev/signin/verify",
            json=json,
            headers=headers,
            timeout=5,
        )
        capture_message(f"Their response was: {response}")
        body = response.json()
        capture_message(f"This is the body: {body}")
        capture_message(f"This is the body jsonified: {jsonify(body)}")

        # if body.get("success"):
        #     print("Successfully verified sign-in for user:", body)
        #     # Set a cookie/userid or perform additional logic here
        # else:
        #     print("Sign-in failed:", body)

        return jsonify(body)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
