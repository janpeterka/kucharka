"""Add event people count

Revision ID: 8e467f58dae6
Revises: 802a72a2ecb3
Create Date: 2021-05-10 19:24:45.572982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8e467f58dae6"
down_revision = "802a72a2ecb3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("events", sa.Column("people_count", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("events", "people_count")
    # ### end Alembic commands ###
