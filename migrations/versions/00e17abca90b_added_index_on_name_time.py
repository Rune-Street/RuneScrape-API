"""Added index on (name, time)

Revision ID: 00e17abca90b
Revises: 1e3567d579ab
Create Date: 2020-04-11 16:12:40.632663

"""
from alembic import op
import sqlalchemy as sa


Session = sa.orm.sessionmaker()


# revision identifiers, used by Alembic.
revision = '00e17abca90b'
down_revision = '1e3567d579ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('price_data_time_idx', table_name='price_data')
    # ### end Alembic commands ###

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "CREATE INDEX price_data_name_time_idx ON price_data(name DESC, time ASC);")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('price_data_time_idx', 'price_data',
                    ['time'], unique=False)
    # ### end Alembic commands ###

    op.drop_index('price_data_name_time_idx', table_name='price_data')
