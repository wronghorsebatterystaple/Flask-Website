"""explicitly set nullable and defaults

Revision ID: 354e7f5e42eb
Revises: 07ecff8bab56
Create Date: 2024-09-30 01:33:07.727042

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '354e7f5e42eb'
down_revision = '07ecff8bab56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_all_posts', sa.Boolean(), nullable=False))
        batch_op.alter_column(column_name='login_required', new_column_name='is_login_required', existing_type=sa.Boolean, nullable=False)
        batch_op.alter_column(column_name='published', new_column_name='is_published', existing_type=sa.Boolean, nullable=False)
        batch_op.alter_column(column_name='writeable', new_column_name='is_writeable', existing_type=sa.Boolean, nullable=False)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column(column_name='unread', new_column_name='is_unread', existing_type=sa.Boolean, nullable=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column(column_name='published', new_column_name='is_published', existing_type=sa.Boolean, nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column(column_name='is_published', new_column_name='published', existing_type=sa.Boolean, nullable=False)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column(column_name='is_unread', new_column_name='unread', existing_type=sa.Boolean, nullable=False)

    with op.batch_alter_table('blogpage', schema=None) as batch_op:
        batch_op.alter_column(column_name='is_login_required', new_column_name='login_required', existing_type=sa.Boolean, nullable=False)
        batch_op.alter_column(column_name='is_published', new_column_name='published', existing_type=sa.Boolean, nullable=False)
        batch_op.alter_column(column_name='is_writeable', new_column_name='writeable', existing_type=sa.Boolean, nullable=False)
        batch_op.drop_column('is_all_posts')

    # ### end Alembic commands ###
