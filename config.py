import os


class Config(object):
    # UPLOAD_FOLDER = "/temporary"
    # ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_STRING")
    # SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 5}
    # SQLALCHEMY_POOL_SIZE = 5

    APP_STATE = os.environ.get("APP_STATE")  # production, development, debug, shutdown

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    SECURITY_CONFIRMABLE = False

    SECURITY_CHANGEABLE = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_RECOVERABLE = True
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = (
        "Žádost o reset hesla do Skautské kuchařky"  # nosec
    )
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
    # SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = "Vaše heslo do Skautské kuchařky bylo resetováno."

    # TURBO_WEBSOCKET_ROUTE = None

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    STORAGE_SYSTEM = os.getenv("STORAGE_SYSTEM", "LOCAL")

    DROPZONE_MAX_FILE_SIZE = 20

    SENTRY_MONITORING = True
    INFO_USED_DB = "production db"

    FF_GALLERY = os.getenv("FF_GALLERY", False)
    FF_GOOGLE_OAUTH = os.getenv("FF_GOOGLE_OAUTH", True)

    SYSTEM_MESSAGE = os.getenv("SYSTEM_MESSAGE", None)


class LocalProdConfig(Config):
    INFO_USED_DB = "production db"
    TEMPLATES_AUTO_RELOAD = True


class DevConfig(LocalProdConfig):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DB_STRING")
    SENTRY_MONITORING = False

    INFO_USED_DB = "local db"
    FLASK_DEBUG = True
    # SQLALCHEMY_ECHO = True
    # EXPLAIN_TEMPLATE_LOADING = True


class TestConfig(Config):
    APP_STATE = "testing"

    TESTING = True
    WTF_CSRF_ENABLED = False
    SENTRY_MONITORING = False
    FLASK_DEBUG = False

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "justtesting"  # nosec
    SECURITY_PASSWORD_SALT = "justtesting"  # nosec

    INFO_USED_DB = "testing db"


class ProdConfig(Config):
    INFO_USED_DB = "production db"
    FLASK_ENV = "production"


configs = {
    "development": DevConfig,
    "test": TestConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "local_production": LocalProdConfig,
    "default": ProdConfig,
}
