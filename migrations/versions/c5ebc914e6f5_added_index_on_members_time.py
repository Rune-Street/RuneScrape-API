"""Added index on (members, time)

Revision ID: c5ebc914e6f5
Revises: 00e17abca90b
Create Date: 2020-04-12 15:05:09.534633

"""
from alembic import op
import sqlalchemy as sa


Session = sa.orm.sessionmaker()


# revision identifiers, used by Alembic.
revision = 'c5ebc914e6f5'
down_revision = '00e17abca90b'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(
        "CREATE INDEX price_data_members_time_idx ON price_data(members DESC, time ASC);")


def downgrade():
    op.drop_index('price_data_members_time_idx', table_name='price_data')
