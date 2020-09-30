import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask settings
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

#  Flask-WTF settings
WTF_CSRF_ENABLED = True  # Activates cross-site request forgery prevention (CSRF)
SECRET_KEY = os.environ.get('SECRET_KEY')  # Secret key used for CSRF

# Flask-SQLAlchemy settings
# sqlite3
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # Path to database file
SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_CYAN_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  # SQLAlchemy-migrate data file directory


# mail server settings
# MAIL_SERVER = c.MAIL_HOST
# MAIL_PORT = c.MAIL_PORT
# MAIL_USERNAME = c.MAIL_USERNAME
# MAIL_PASSWORD = c.MAIL_PASSWORD

# administrator list
# ADMINS = c.ADMINS

# stream api
TWITCH_API_CLIENT_ID = os.environ.get('TWITCH_API_CLIENT_ID')
TWITCH_API_CLIENT_SECRET = os.environ.get('TWITCH_API_CLIENT_SECRET')
TWITCH_API_STREAM_URL = 'https://api.twitch.tv/kraken/streams/?channel='
