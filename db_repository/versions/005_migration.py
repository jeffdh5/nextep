from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
followers = Table('followers', pre_meta,
    Column('follower_id', Integer),
    Column('followed_show_id', Integer),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('show_id', Integer),
)

show = Table('show', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('day_of_week', String(length=64)),
    Column('tv_link', String(length=64)),
    Column('tv_rage_link', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].columns['followed_show_id'].drop()
    post_meta.tables['followers'].columns['show_id'].create()
    post_meta.tables['show'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['followers'].columns['followed_show_id'].create()
    post_meta.tables['followers'].columns['show_id'].drop()
    post_meta.tables['show'].columns['name'].drop()
