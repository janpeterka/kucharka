"""Add portion count

Revision ID: 097c679b21fc
Revises: 87ad3738f932
Create Date: 2021-07-02 16:38:16.053401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "097c679b21fc"
down_revision = "87ad3738f932"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "daily_plans_have_recipes",
        sa.Column("portion_count", sa.Integer(), nullable=False),
    )


def downgrade():
    op.drop_column("daily_plans_have_recipes", "portion_count")
