"""Fill missing ingredients.create_at

Revision ID: a334a3a614a7
Revises: 93034edd5318
Create Date: 2023-06-28 17:37:33.258555

"""
from alembic import op

# import sqlalchemy as sa
# from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "a334a3a614a7"
down_revision = "93034edd5318"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        UPDATE ingredients
            SET created_at = '2000-01-01 00:00:00'
            WHERE created_at IS NULL;
        """
    )


def downgrade():
    pass
