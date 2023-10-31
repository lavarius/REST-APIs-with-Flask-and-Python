"""empty message

Revision ID: 8373ad588657
Revises: 0e8abee71a76
Create Date: 2023-10-31 14:54:12.968338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8373ad588657'
down_revision = '0e8abee71a76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
