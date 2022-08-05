"""Change portion_count to float

Revision ID: 71405264f03b
Revises: 88f96c0ea05c
Create Date: 2022-08-02 18:49:41.355772

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "71405264f03b"
down_revision = "88f96c0ea05c"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "daily_plans_have_recipes",
        "portion_count",
        type_=mysql.FLOAT(),
    )


def downgrade():
    op.alter_column(
        "daily_plans_have_recipes",
        "portion_count",
        type_=mysql.INTEGER(),
    )
