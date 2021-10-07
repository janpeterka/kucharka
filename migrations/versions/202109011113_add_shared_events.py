"""Add shared events

Revision ID: 8d5c55c559f0
Revises: 1dd7f127a503
Create Date: 2021-09-01 11:13:34.759640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8d5c55c559f0"
down_revision = "1dd7f127a503"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("events", sa.Column("is_shared", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("events", "is_shared")
    # ### end Alembic commands ###
