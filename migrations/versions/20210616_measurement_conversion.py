"""Add measurement to measurement conversion

Revision ID: 87ad3738f932
Revises: 16f0477115fa
Create Date: 2021-06-16 15:15:02.349235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "87ad3738f932"
down_revision = "16f0477115fa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurements_to_measurements",
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("to_measurement_id", sa.Integer(), nullable=False),
        sa.Column("amount_from", sa.Float(), nullable=True),
        sa.Column("amount_to", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["ingredient_id"], ["ingredients.id"]),
        sa.ForeignKeyConstraint(["to_measurement_id"], ["measurements.id"]),
        sa.PrimaryKeyConstraint("ingredient_id", "to_measurement_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("measurements_to_measurements")
    # ### end Alembic commands ###
