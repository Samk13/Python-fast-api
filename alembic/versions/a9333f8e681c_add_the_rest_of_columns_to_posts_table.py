"""add the rest of columns to posts table

Revision ID: a9333f8e681c
Revises: 265d61ecbf99
Create Date: 2021-11-24 22:58:28.876862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a9333f8e681c"
down_revision = "265d61ecbf99"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "published", sa.Boolean, nullable=False, server_default=sa.text("True")
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")

    pass
