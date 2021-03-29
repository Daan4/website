import os

from config import website_test_config as c

basedir = os.path.abspath(os.path.dirname(__file__))

#  Flask-WTF settings
WTF_CSRF_ENABLED = False  # Activates cross-site request forgery prevention (CSRF)
SECRET_KEY = c.SECRET_KEY  # Secret key used for CSRF

# Flask-SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = c.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # SQLAlchemy-migrate data file directory

# testing
TESTING = True
