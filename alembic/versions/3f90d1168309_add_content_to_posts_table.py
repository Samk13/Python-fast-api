# -*- coding: utf-8 -*-
"""add content to posts table

Revision ID: 3f90d1168309
Revises: ea8977276f3f
Create Date: 2021-11-24 22:38:17.020674

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "3f90d1168309"
down_revision = "ea8977276f3f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(length=255), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
