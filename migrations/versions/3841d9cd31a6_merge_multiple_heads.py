"""Merge multiple heads

Revision ID: 3841d9cd31a6
Revises: 14eb49aadc9b, 18ee311fd7a6
Create Date: 2023-11-08 15:14:59.495721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3841d9cd31a6'
down_revision = ('14eb49aadc9b', '18ee311fd7a6')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
