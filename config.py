import os


class Config(object):
    # UPLOAD_FOLDER = "/temporary"
    # ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_STRING")

    APP_STATE = os.environ.get("APP_STATE")  # production, development, debug, shutdown

    SECURITY_PASSWORD_SALT = os.environ.get("SECRET_KEY")
    SECURITY_REGISTERABLE = True

    # SENTRY_MONITORING = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DB_STRING")
    APP_STATE = os.environ.get(
        "TESTING_APP_STATE"
    )  # production, development, debug, shutdown
    SECRET_KEY = os.environ.get("TESTING_SECRET_KEY")
    # SENTRY_MONITORING = False


class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DB_STRING")
    # SQLALCHEMY_ECHO = True
    APP_STATE = os.environ.get(
        "LOCAL_APP_STATE"
    )  # production, development, debug, shutdown
    # SENTRY_MONITORING = False


class ProdConfig(Config):
    pass


configs = {
    "development": DevConfig,
    "test": TestConfig,
    "production": ProdConfig,
    "default": ProdConfig,
}
