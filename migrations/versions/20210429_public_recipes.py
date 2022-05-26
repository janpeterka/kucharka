"""Enable public recipes

Revision ID: 1b0f7ab86df8
Revises: 1807553a5c77
Create Date: 2021-04-29 16:33:26.220642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b0f7ab86df8"
down_revision = "1807553a5c77"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("recipes", sa.Column("is_public", sa.Boolean(), nullable=True))
    op.add_column("recipes", sa.Column("is_shared", sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column("recipes", "is_public")
    op.drop_column("recipes", "is_shared")
