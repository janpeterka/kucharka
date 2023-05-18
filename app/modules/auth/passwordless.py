import requests
from flask import jsonify, request, Blueprint
from flask import current_app as app
from flask_security import current_user

passwordless = Blueprint("passwordless", __name__)


@passwordless.route("register-token")
def register_token():
    print("trying to add token...")

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
    )
    print(response.__dict__)
    print(response.json())
    token = response.json().get("token")
    # Process the token or perform any additional logic here
    return {"token": token}


# @passwordless.route("/signin/verify", methods=["POST"])
# def verify_sign_in():
#     try:
#         token = request.json.get("token")

#         api_secret = app.config["PASSWORDLESS_SECRET"]
#         headers = {"ApiSecret": api_secret, "Content-Type": "application/json"}
#         response = requests.post(
#             "https://v4.passwordless.dev/signin/verify", json=token, headers=headers
#         )
#         body = response.json()

#         if body.get("success"):
#             print("Successfully verified sign-in for user:", body)
#             # Set a cookie/userid or perform additional logic here
#         else:
#             print("Sign-in failed:", body)

#         return jsonify(body)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
