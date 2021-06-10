"""Add info about lasting ingredient categories

Revision ID: 16f0477115fa
Revises: 10229b767711
Create Date: 2021-06-10 15:40:56.493755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "16f0477115fa"
down_revision = "10229b767711"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "ingredient_categories", sa.Column("is_lasting", sa.Boolean(), nullable=True)
    )


def downgrade():
    op.drop_column("ingredient_categories", "is_lasting")
