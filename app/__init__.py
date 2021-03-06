from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from turbo_flask import Turbo
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_dropzone import Dropzone
from flask_sqlalchemy.model import DefaultMeta  # noqa: E402
from sqlalchemy import MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(
    session_options={"autoflush": False},
    metadata=MetaData(naming_convention=convention),
)
turbo = Turbo()

BaseModel: DefaultMeta = db.Model

from app.models.users import User  # noqa: E402
from app.models.roles import Role  # noqa: E402

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

migrate = Migrate()
babel = Babel()
mail = Mail()
security = Security()
dropzone = Dropzone()


def create_app(config_name="default"):
    application = Flask(__name__, instance_relative_config=True)

    from jinja2 import select_autoescape

    # CONFIG
    from config import configs

    application.config.from_object(configs[config_name])

    print(f"DB INFO: using {application.config['INFO_USED_DB']}")

    # APPS
    db.init_app(application)
    migrate.init_app(application, db)
    security.init_app(application, user_datastore)
    babel.init_app(application)
    turbo.init_app(application)
    mail.init_app(application)
    dropzone.init_app(application)

    if application.config["SENTRY_MONITORING"]:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn="https://e50dbd5c633a43dda2d9d4d0ae2475ad@o457759.ingest.sentry.io/5776351",
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
            traces_sample_rate=1.0,
        )
    else:
        print("No Sentry monitoring.")

    # LOGGING
    # from .config.config_logging import db_handler, gunicorn_logger

    # application.logger.addHandler(gunicorn_logger)
    # application.logger.addHandler(db_handler)

    # CONTROLLERS
    from .controllers import register_all_controllers  # noqa: F401

    register_all_controllers(application)

    from .controllers import register_error_handlers  # noqa: F401

    register_error_handlers(application)

    # MODULES
    from app.modules.auth.auth import blueprint as google_oauth_bp

    application.register_blueprint(google_oauth_bp, url_prefix="/oauth/")

    if application.config["APP_STATE"] in ("test", "testing"):
        with application.app_context():
            # from app.helpers.tests.fill_db import db_fill
            db.create_all()
            print("Created database")

            # db_fill()

    application.jinja_options = {
        "autoescape": select_autoescape(enabled_extensions=("html", "html.j2", "xml")),
        "line_statement_prefix": "#",
        "line_comment_prefix": "##",
    }

    return application
