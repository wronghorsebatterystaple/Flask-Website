"""sqlalchemy relationships

Revision ID: 4dd6d05f0e21
Revises: 4ad27741108d
Create Date: 2024-03-11 04:21:44.888847

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4dd6d05f0e21'
down_revision = '4ad27741108d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
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

    # ### end Alembic commands ###
