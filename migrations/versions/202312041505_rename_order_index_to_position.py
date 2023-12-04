"""Rename order_index to position

Revision ID: 3cd8a2bfb2fd
Revises: 8ee949e8722c
Create Date: 2023-12-04 15:05:06.415112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3cd8a2bfb2fd'
down_revision = '8ee949e8722c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("daily_plans_have_recipes") as batch_op:
        batch_op.alter_column(
            "order_index", new_column_name="position", type_=sa.Integer
        )


def downgrade():
    with op.batch_alter_table("daily_plans_have_recipes") as batch_op:
        batch_op.alter_column(
            "position", new_column_name="order_index", type_=sa.Integer
        )
