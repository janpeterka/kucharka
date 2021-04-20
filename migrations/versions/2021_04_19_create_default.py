"""Create default scheme

Revision ID: 31068afb5695
Revises:
Create Date: 2021-04-20 22:27:12.328597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "31068afb5695"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "users",
        sa.Column("fs_uniquifier", sa.String(length=64), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("current_login_at", sa.DateTime(), nullable=True),
        sa.Column("last_login_ip", sa.String(length=64), nullable=True),
        sa.Column("current_login_ip", sa.String(length=64), nullable=True),
        sa.Column("login_count", sa.Integer(), nullable=True),
        sa.Column("tf_primary_method", sa.String(length=64), nullable=True),
        sa.Column("tf_totp_secret", sa.String(length=255), nullable=True),
        sa.Column("tf_phone_number", sa.String(length=128), nullable=True),
        sa.Column(
            "create_datetime",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_datetime",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("us_totp_secrets", sa.Text(), nullable=True),
        sa.Column("us_phone_number", sa.String(length=128), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("fs_uniquifier"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("measurement", sa.Integer(), nullable=False),
        sa.Column("calorie", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("sugar", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("fat", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.Column("protein", sa.Float(), server_default=sa.text("'0'"), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["measurement"], ["measurements.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ingredients_created_by"), "ingredients", ["created_by"], unique=False
    )
    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_recipes_created_by"), "recipes", ["created_by"], unique=False
    )
    op.create_table(
        "users_have_roles",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_table(
        "recipes_have_ingredients",
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["ingredient_id"], ["ingredients.id"]),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"]),
        sa.PrimaryKeyConstraint("recipe_id", "ingredient_id"),
    )
    op.create_index(
        op.f("ix_recipes_have_ingredients_ingredient_id"),
        "recipes_have_ingredients",
        ["ingredient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_recipes_have_ingredients_recipe_id"),
        "recipes_have_ingredients",
        ["recipe_id"],
        unique=False,
    )


def downgrade():
    op.drop_table("recipes_have_ingredients")
    op.drop_table("users_have_roles")
    op.drop_table("recipes")
    op.drop_table("ingredients")
    op.drop_table("users")
    op.drop_table("roles")
