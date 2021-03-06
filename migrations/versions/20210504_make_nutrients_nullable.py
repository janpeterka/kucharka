"""Make ingredient nutriens nullable

Revision ID: d8bce65702d3
Revises: 27bb148ce353
Create Date: 2021-05-04 13:51:39.297977

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "d8bce65702d3"
down_revision = "27bb148ce353"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ingredients",
        "calorie",
        existing_type=mysql.FLOAT(),
        nullable=True,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "fat",
        existing_type=mysql.FLOAT(),
        nullable=True,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "protein",
        existing_type=mysql.FLOAT(),
        nullable=True,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "sugar",
        existing_type=mysql.FLOAT(),
        nullable=True,
        existing_server_default=sa.text("'0'"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ingredients",
        "sugar",
        existing_type=mysql.FLOAT(),
        nullable=False,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "protein",
        existing_type=mysql.FLOAT(),
        nullable=False,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "fat",
        existing_type=mysql.FLOAT(),
        nullable=False,
        existing_server_default=sa.text("'0'"),
    )
    op.alter_column(
        "ingredients",
        "calorie",
        existing_type=mysql.FLOAT(),
        nullable=False,
        existing_server_default=sa.text("'0'"),
    )
    # ### end Alembic commands ###
