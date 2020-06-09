"""Added index on (members, time)

Revision ID: c5ebc914e6f5
Revises: 00e17abca90b
Create Date: 2020-04-12 15:05:09.534633

"""
import sqlalchemy as sa
from alembic import op

Session = sa.orm.sessionmaker()


# revision identifiers, used by Alembic.
revision = 'c5ebc914e6f5'
down_revision = '00e17abca90b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('price_data_members_time_idx', 'price_data', [
                    sa.text('members DESC'), 'time'], unique=False)


def downgrade():
    op.drop_index('price_data_members_time_idx', table_name='price_data')
