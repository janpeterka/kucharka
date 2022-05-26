"""Add events

Revision ID: 2e4f3a3214d8
Revises: d8bce65702d3
Create Date: 2021-05-10 16:13:55.529508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e4f3a3214d8"
down_revision = "d8bce65702d3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_events_created_by"), "events", ["created_by"], unique=False
    )
    op.add_column("daily_plans", sa.Column("event_id", sa.Integer(), nullable=True))


def downgrade():
    op.drop_column("daily_plans", "event_id")
    op.drop_table("events")
