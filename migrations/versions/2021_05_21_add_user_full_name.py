"""Add user full name

Revision ID: 329e87196a48
Revises: 54307bd50389
Create Date: 2021-05-02 14:42:35.164456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "329e87196a48"
down_revision = "54307bd50389"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("full_name", sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column("users", "full_name")
