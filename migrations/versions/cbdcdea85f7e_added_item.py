"""Added item

Revision ID: cbdcdea85f7e
Revises: 
Create Date: 2020-04-02 22:23:55.780727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbdcdea85f7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('price_data',
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('members', sa.Boolean(), nullable=False),
    sa.Column('buy_average', sa.Integer(), nullable=False),
    sa.Column('buy_quantity', sa.Integer(), nullable=False),
    sa.Column('sell_average', sa.Integer(), nullable=False),
    sa.Column('sell_quantity', sa.Integer(), nullable=False),
    sa.Column('overall_average', sa.Integer(), nullable=False),
    sa.Column('overall_quantity', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(timezone=True), server_default=sa.text("date_trunc('hour', NOW()) + INTERVAL '5 min' * ROUND(date_part('minute', NOW()) / 5.0)"), nullable=False),
    sa.PrimaryKeyConstraint('pk'),
    sa.UniqueConstraint('pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_data')
    # ### end Alembic commands ###
