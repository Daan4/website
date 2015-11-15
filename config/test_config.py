import os

from config import website_test_config as c

basedir = os.path.abspath(os.path.dirname(__file__))

#  Flask-WTF settings
WTF_CSRF_ENABLED = False  # Activates cross-site request forgery prevention (CSRF)
SECRET_KEY = c.SECRET_KEY  # Secret key used for CSRF

# Flask-SQLAlchemy settings
# sqlite3
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Path to database file
SQLALCHEMY_DATABASE_URI = c.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # SQLAlchemy-migrate data file directory


# mail server settings
MAIL_SERVER = c.MAIL_HOST
MAIL_PORT = c.MAIL_PORT
MAIL_USERNAME = c.MAIL_USERNAME
MAIL_PASSWORD = c.MAIL_PASSWORD

# administrator list
ADMINS = c.ADMINS

# stream api
TWITCH_API_CLIENT_ID = c.TWITCH_API_CLIENT_ID
TWITCH_API_CLIENT_SECRET = c.TWITCH_API_CLIENT_SECRET
TWITCH_API_STREAM_URL = 'https://api.twitch.tv/kraken/streams/?channel='

# testing
TESTING = True
