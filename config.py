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

    SECURITY_CHANGEABLE = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_RECOVERABLE = True
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = "Žádost o reset hesla do Skautské kuchařky"
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
    # SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = "Vaše heslo do Skautské kuchařky bylo resetováno."

    TURBO_WEBSOCKET_ROUTE = None

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    SENTRY_MONITORING = True
    INFO_USED_DB = "production db"


class LocalProdConfig(Config):
    INFO_USED_DB = "production db"
    TEMPLATES_AUTO_RELOAD = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DB_STRING")
    SECRET_KEY = os.environ.get("TESTING_SECRET_KEY")
    SENTRY_MONITORING = False

    INFO_USED_DB = "testing db"


class DevConfig(LocalProdConfig):
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("LOCAL_DB_STRING")
    SENTRY_MONITORING = False

    INFO_USED_DB = "local db"
    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    INFO_USED_DB = "production db"


configs = {
    "development": DevConfig,
    "test": TestConfig,
    "production": ProdConfig,
    "local_production": LocalProdConfig,
    "default": ProdConfig,
}
