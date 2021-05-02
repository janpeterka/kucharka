"""Add recipe categories

Revision ID: 06bdf14c5de1
Revises: 329e87196a48
Create Date: 2021-05-02 21:50:21.052923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06bdf14c5de1"
down_revision = "329e87196a48"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "recipe_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )


def downgrade():
    op.drop_table("recipe_categories")
