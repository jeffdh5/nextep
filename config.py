import os

SECRET_KEY = 'gvz1736sua6rg4djstg38856mf7sjgylsasmhfh2bddxyex5o2s60ovolmvyx7qrj897zx2tsdlro9vyiwiyxgksqz14kpryl3vq'

#Flask - SQLAlchemy setup
basedir = os.path.abspath(os.path.dirname(__file__))

#joins pathname get a database - turns into
#sqlite:///app/app.db.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') 

#Location of the migration files.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') 

