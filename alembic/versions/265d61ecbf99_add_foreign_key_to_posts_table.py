"""add foreign key to posts table

Revision ID: 265d61ecbf99
Revises: 360bda0494c8
Create Date: 2021-11-24 22:50:12.068847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "265d61ecbf99"
down_revision = "360bda0494c8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
