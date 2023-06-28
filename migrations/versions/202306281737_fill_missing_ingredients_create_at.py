"""Fill missing ingredients.create_at

Revision ID: a334a3a614a7
Revises: 93034edd5318
Create Date: 2023-06-28 17:37:33.258555

"""
# from alembic import op
# import sqlalchemy as sa
# from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "a334a3a614a7"
down_revision = "93034edd5318"
branch_labels = None
depends_on = None


def upgrade():
    from app.models import Ingredient
    import datetime

    for i in Ingredient.load_all():
        if not i.created_at:
            i.created_at = datetime.datetime(2000, 1, 1)
            i.edit()


def downgrade():
    pass
