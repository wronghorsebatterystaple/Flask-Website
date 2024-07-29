"""fully convert to utf8mb4 support

Revision ID: 41c3e9dcdfce
Revises: edd132b78832
Create Date: 2024-07-29 10:06:18.404094

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '41c3e9dcdfce'
down_revision = 'edd132b78832'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_bin', length=100),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_bin', length=100),
               existing_nullable=False)
        batch_op.alter_column('content',
               existing_type=mysql.TEXT(charset='utf8mb3', collation='utf8mb3_bin'),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_bin', length=5000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_bin', length=5000),
               type_=mysql.TEXT(charset='utf8mb3', collation='utf8mb3_bin'),
               existing_nullable=False)
        batch_op.alter_column('author',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_bin', length=100),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_bin', length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
