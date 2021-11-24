"""Add user table

Revision ID: 360bda0494c8
Revises: 3f90d1168309
Create Date: 2021-11-24 22:43:37.879017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "360bda0494c8"
down_revision = "3f90d1168309"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
