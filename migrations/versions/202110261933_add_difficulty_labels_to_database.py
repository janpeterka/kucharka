"""Add difficulty labels to database

Revision ID: d2e3a789a0e7
Revises: 34958ef8528c
Create Date: 2021-10-26 19:33:13.800374

"""
from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d2e3a789a0e7"
down_revision = "34958ef8528c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO
            `label_categories` (`id`, `name`, `description`, `allow_multiple`)
        VALUES
            (2, 'difficulty', 'obtížnost přípravy', 0);
        """
    )

    op.execute(
        """
        INSERT INTO
            `labels` (`id`,`name`,`description`,`category_id`,`visible_name`, `color`)
        VALUES
            (5,'easy',NULL,2,'snadné', 'light-green'),
            (6,'medium',NULL,2,'pokročilé', 'light-yellow'),
            (7,'hard',NULL,2,'obtížné', 'light-red')
        """
    )


def downgrade():
    op.execute(
        """
        DELETE FROM
            `recipes_have_labels`
        WHERE
            label_id IN (5,6,7)
        """
    )

    op.execute(
        """
        DELETE FROM
            `labels`
        WHERE
            id IN (5,6,7)
        """
    )

    op.execute(
        """
        DELETE FROM
            `label_categories`
        WHERE
            id = 2
        """
    )
