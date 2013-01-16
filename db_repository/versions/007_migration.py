from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
followers = Table('followers', pre_meta,
    Column('follower_id', Integer),
    Column('show_id', Integer),
)

show = Table('show', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('day_of_week', String),
    Column('tv_link', String),
    Column('tv_rage_link', String),
    Column('name', String),
)

show = Table('show', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('day', String(length=64)),
    Column('tv_link', String(length=64)),
    Column('tv_rage_link', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].drop()
    pre_meta.tables['show'].columns['day_of_week'].drop()
    post_meta.tables['show'].columns['day'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].create()
    pre_meta.tables['show'].columns['day_of_week'].create()
    post_meta.tables['show'].columns['day'].drop()
