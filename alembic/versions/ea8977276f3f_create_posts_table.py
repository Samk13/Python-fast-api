# -*- coding: utf-8 -*-
"""create posts table

Revision ID: ea8977276f3f
Revises:
Create Date: 2021-11-24 22:28:39.657093

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ea8977276f3f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        # sa.Column('content', sa.String(length=255), nullable=False),
        # sa.Column('published', sa.Boolean,
        #           server_default="True", nullable=False),
        # sa.Column('created_at', sa.TIMESTAMP(timezone=True),
        #           nullable=False, server_default=sa.text("now()")),
        # sa.Column('owner_id', sa.Integer, sa.ForeignKey(
        #     'users.id', ondelete='CASCADE'), nullable=False)
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
