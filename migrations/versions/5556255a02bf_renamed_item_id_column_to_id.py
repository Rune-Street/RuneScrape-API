"""Renamed item_id column to id

Revision ID: 5556255a02bf
Revises: 373012ff4dd0
Create Date: 2020-04-03 22:01:07.300178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5556255a02bf'
down_revision = '373012ff4dd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('price_data', sa.Column('id', sa.Integer(), nullable=False))
    # op.drop_column('price_data', 'item_id')
    # ### end Alembic commands ###
    op.alter_column('price_data', 'item_id', new_column_name='id')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('price_data', sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # op.drop_column('price_data', 'id')
    # ### end Alembic commands ###
    op.alter_column('price_data', 'id', new_column_name='item_id')
