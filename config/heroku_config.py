import os

basedir = os.path.abspath(os.path.dirname(__file__))

#  Flask-WTF settings
WTF_CSRF_ENABLED = True  # Activates cross-site request forgery prevention (CSRF)
SECRET_KEY = os.environ.get('SECRET_KEY')  # Secret key used for CSRF

# Flask-SQLAlchemy settings
# For the URI postgres:// is deprecated and replaced by postgresql:// ,
# however changing the config var involves removing the postgres addon so therefore this replacement instead.
SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_CYAN_URL').replace('postgres://', 'postgresql://')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # SQLAlchemy-migrate data file directory

# Flask settings
SESSION_COOKIE_SAMESITE = 'STRICT'

# Nano settings
NANO_NODE_IP = '65.21.110.208'
