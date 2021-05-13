import os


class Config(object):
    # UPLOAD_FOLDER = "/temporary"
    # ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_STRING")
    SQLALCHEMY_POOL_SIZE = 5

    APP_STATE = os.environ.get("APP_STATE")  # production, development, debug, shutdown

    SECURITY_PASSWORD_SALT = os.environ.get("SECRET_KEY")
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_CONFIRMABLE = False

    # SENTRY_MONITORING = True
    INFO_USED_DB = "production db"


class LocalProdConfig(Config):
    INFO_USED_DB = "production db"
    TEMPLATES_AUTO_RELOAD = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DB_STRING")
    APP_STATE = os.environ.get("TESTING_APP_STATE")
    SECRET_KEY = os.environ.get("TESTING_SECRET_KEY")
    # SENTRY_MONITORING = False

    INFO_USED_DB = "testing db"


class DevConfig(LocalProdConfig):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DB_STRING")
    # SQLALCHEMY_ECHO = True
    # APP_STATE = os.environ.get("LOCAL_APP_STATE")
    # SENTRY_MONITORING = False

    INFO_USED_DB = "local db"


class ProdConfig(Config):
    INFO_USED_DB = "production db"


configs = {
    "development": DevConfig,
    "test": TestConfig,
    "production": ProdConfig,
    "local_production": LocalProdConfig,
    "default": ProdConfig,
}
