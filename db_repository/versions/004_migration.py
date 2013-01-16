from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
show = Table('show', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('day_of_week', String(length=64)),
    Column('tv_link', String(length=64)),
    Column('tv_rage_link', String(length=64)),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('followed_show_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['show'].create()
    post_meta.tables['followers'].columns['followed_show_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['show'].drop()
    post_meta.tables['followers'].columns['followed_show_id'].drop()
