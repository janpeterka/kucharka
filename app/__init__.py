from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    # UserMixin,
    # RoleMixin,
    login_required,
)


# import pymysql
# import numpy as np

# pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
# pymysql.converters.conversions = pymysql.converters.encoders.copy()
# pymysql.converters.conversions.update(pymysql.converters.decoders)

db = SQLAlchemy(session_options={"autoflush": False, "autocommit": False})
migrate = Migrate()

from app.models.users import User
from app.models.roles import Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app(config_name="default"):
    application = Flask(__name__, instance_relative_config=True)

    # CONFIG
    from config import configs

    application.config.from_object(configs[config_name])

    # APPS
    db.init_app(application)
    migrate.init_app(application, db)
    security = Security(application, user_datastore)

    # if application.config["SENTRY_MONITORING"]:
    #     import sentry_sdk
    #     from sentry_sdk.integrations.flask import FlaskIntegration
    #     from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    #     sentry_sdk.init(
    #         dsn="https://cf0294c7f1784ba2acbe5c9ed2409bef@o457759.ingest.sentry.io/5454190",
    #         integrations=[FlaskIntegration(), SqlalchemyIntegration()],
    #         traces_sample_rate=0.2,
    #     )
    # else:
    #     print("No Sentry monitoring.")

    # LOGGING
    # from .config.config_logging import db_handler, gunicorn_logger

    # application.logger.addHandler(gunicorn_logger)
    # application.logger.addHandler(db_handler)

    # CONTROLLERS
    from .controllers import register_all_controllers  # noqa: F401

    register_all_controllers(application)

    # from .controllers import register_error_handlers  # noqa: F401

    # register_error_handlers(application)

    return application
