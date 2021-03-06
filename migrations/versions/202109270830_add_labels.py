"""Add labels

Revision ID: 85fc374dd038
Revises: 8d5c55c559f0
Create Date: 2021-09-27 08:30:19.123693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "85fc374dd038"
down_revision = "8d5c55c559f0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "label_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "labels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("visible_name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["label_categories.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("visible_name"),
    )
    op.create_table(
        "recipes_have_labels",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("label_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["label_id"], ["labels.id"]),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        """
        INSERT INTO
            `label_categories` (`id`, `name`, `description`)
        VALUES
            (1, 'dietary', 'dietní omezení, alergie');
        """
    )

    op.execute(
        """
        INSERT INTO
            `labels` (`id`,`name`,`description`,`category_id`,`visible_name`)
        VALUES
            (1,'vegetarian',NULL,1,'vegetariánské'),
            (2,'vegan',NULL,1,'veganské'),
            (3,'gluten_free',NULL,1,'bez lepku'),
            (4,'lactose_free',NULL,1,'bez laktózy');
        """
    )


def downgrade():
    op.drop_table("recipes_have_labels")
    op.drop_table("labels")
    op.drop_table("label_categories")
