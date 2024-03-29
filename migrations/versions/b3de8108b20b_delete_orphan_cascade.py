"""delete-orphan cascade

Revision ID: b3de8108b20b
Revises: da9f99cb588b
Create Date: 2024-03-11 05:26:53.449899

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b3de8108b20b'
down_revision = 'da9f99cb588b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('comment_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_constraint('image_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'], ondelete='CASCADE')

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

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('image_ibfk_1', 'post', ['post_id'], ['id'])

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comment_ibfk_1', 'post', ['post_id'], ['id'])

    # ### end Alembic commands ###
