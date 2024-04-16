"""add published col to posts

Revision ID: c89491fb413b
Revises: ae934d702e16
Create Date: 2024-04-14 01:09:08.818012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c89491fb413b'
down_revision = 'ae934d702e16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('published', sa.Boolean(), nullable=False))
        batch_op.alter_column('content',
               existing_type=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
               type_=sa.Text(length=100000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.Text(length=100000),
               type_=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
               existing_nullable=False)
        batch_op.drop_column('published')

    # ### end Alembic commands ###