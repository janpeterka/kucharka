"""Add label color

Revision ID: e5512c33b7f9
Revises: 6f81e793e8e6
Create Date: 2021-10-02 11:03:03.071096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e5512c33b7f9"
down_revision = "6f81e793e8e6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("labels", sa.Column("color", sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column("labels", "color")
