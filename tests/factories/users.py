import factory
from flask_security.utils import hash_password
from datetime import datetime

from app import db, security
from app.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    email = factory.Sequence(lambda n: f"user{n}@skautskakucharka.cz")
    password = factory.LazyAttribute(lambda a: hash_password("password"))
    name = factory.Sequence(lambda n: f"User {n}")
    nickname = factory.Sequence(lambda n: f"User {n}")
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = "127.0.0.1"
    current_login_ip = "127.0.0.1"
    created_by = 1
    login_count = 1
    roles = []
    active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return security.datastore.create_user(*args, **kwargs)
