"""made publishing_sibling_id unique

Revision ID: 07ecff8bab56
Revises: 0498bb0f1d52
Create Date: 2024-09-30 00:52:41.807095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07ecff8bab56'
down_revision = '0498bb0f1d52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpage', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['publishing_sibling_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpage', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
