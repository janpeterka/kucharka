"""Add hidden to tips

Revision ID: 1dd7f127a503
Revises: 5c6b8f2d4bd8
Create Date: 2021-07-12 18:30:44.279901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1dd7f127a503"
down_revision = "5c6b8f2d4bd8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tips", sa.Column("is_hidden", sa.Boolean(), nullable=False))


def downgrade():
    op.drop_column("tips", "is_hidden")
