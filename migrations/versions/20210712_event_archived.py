"""Add is_archived to event

Revision ID: 5c6b8f2d4bd8
Revises: 982f6f2cd912
Create Date: 2021-07-12 15:05:54.112242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5c6b8f2d4bd8"
down_revision = "982f6f2cd912"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("events", sa.Column("is_archived", sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column("events", "is_archived")
