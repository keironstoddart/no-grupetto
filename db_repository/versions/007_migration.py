from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
activity = Table('activity', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('athlete_id', Integer),
    Column('bpm', Float),
    Column('strava_id', Integer),
    Column('distance', Float),
    Column('elevation', Float),
    Column('calories', Integer),
    Column('speed', Float),
    Column('max_speed', Float),
    Column('city', String(length=64)),
    Column('state', String(length=64)),
    Column('date', DateTime),
    Column('act_type', String(length=64)),
    Column('name', String(length=64)),
    Column('time', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['activity'].columns['time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['activity'].columns['time'].drop()
