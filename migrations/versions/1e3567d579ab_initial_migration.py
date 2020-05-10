"""Initial migration

Revision ID: 1e3567d579ab
Revises:
Create Date: 2020-04-04 14:30:51.979887

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


# revision identifiers, used by Alembic.
revision = '1e3567d579ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('price_data',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('members', sa.Boolean(), nullable=False),
                    sa.Column('buy_average', sa.Integer(), nullable=False),
                    sa.Column('buy_quantity', sa.Integer(), nullable=False),
                    sa.Column('sell_average', sa.Integer(), nullable=False),
                    sa.Column('sell_quantity', sa.Integer(), nullable=False),
                    sa.Column('overall_average', sa.Integer(), nullable=False),
                    sa.Column('overall_quantity',
                              sa.Integer(), nullable=False),
                    sa.Column('time', sa.DateTime(timezone=True), server_default=sa.text(
                        "date_trunc('hour', NOW()) + INTERVAL '5 min' * ROUND(date_part('minute', NOW()) / 5.0)"), nullable=False),
                    sa.PrimaryKeyConstraint('id', 'time')
                    )
    # ### end Alembic commands ###
    bind = op.get_bind()
    session = Session(bind=bind)
    # chunk_time_interval is in ms
    # Currently set at 21 days per chunk
    session.execute("SELECT create_hypertable(main_table=>'price_data', time_column_name=>'time', chunk_time_interval=>1814400000000, if_not_exists=>TRUE, migrate_data=>TRUE, create_default_indexes=>TRUE);")
    session.execute("ALTER TABLE price_data SET (timescaledb.compress, timescaledb.compress_segmentby = 'id', timescaledb.compress_orderby = 'time DESC');")
    session.execute("SELECT add_compress_chunks_policy('price_data', INTERVAL '28 days');")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('price_data')
    # ### end Alembic commands ###
