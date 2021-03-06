"""Enable public ingredients

Revision ID: 1807553a5c77
Revises: 964fdad8ef3d
Create Date: 2021-04-29 13:22:11.674931

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "1807553a5c77"
down_revision = "964fdad8ef3d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("ingredients", sa.Column("is_public", sa.Boolean(), nullable=True))
    op.add_column(
        "ingredients", sa.Column("source", sa.String(length=255), nullable=True)
    )
    op.alter_column(
        "measurements", "name", existing_type=mysql.VARCHAR(length=80), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "measurements", "name", existing_type=mysql.VARCHAR(length=80), nullable=True
    )
    op.drop_column("ingredients", "source")
    op.drop_column("ingredients", "is_public")
    # ### end Alembic commands ###
