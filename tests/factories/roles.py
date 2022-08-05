import factory

from app import db, security
from app.models import Role


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return security.datastore.create_role(*args, **kwargs)
