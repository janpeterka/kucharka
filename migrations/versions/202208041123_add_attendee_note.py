"""Add attendee note

Revision ID: 32c01362370f
Revises: e0a86e5d519e
Create Date: 2022-08-04 11:23:33.925181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "32c01362370f"
down_revision = "e0a86e5d519e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("attendees", sa.Column("note", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("attendees", "note")
    # ### end Alembic commands ###