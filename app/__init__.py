from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import *

# Flask
app = Flask(__name__)
app.config.from_object('config')

# SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# navigation
from app import navigation
nav = navigation.Navigation(app)
navigation.init_navigation(nav)


# Error handling
import logging

# if not app.debug:
#     # Via email
#     from logging.handlers import SMTPHandler
#     credentials = None
#     if MAIL_USERNAME or MAIL_PASSWORD:
#         credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#     mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'www.daanlubbers.nl failure', credentials)
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)

from logging.handlers import RotatingFileHandler


class DebugRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode='a', max_bytes=0, backup_count=0, encoding=None, delay=False):
        RotatingFileHandler.__init__(self, filename, mode, max_bytes, backup_count, encoding, delay)

    def emit(self, record):
        if not record.levelno == logging.DEBUG:
            return
        RotatingFileHandler.emit(self, record)

# Via file
# INFO or higher
file_handler = RotatingFileHandler('tmp/website.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
app.logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
# DEBUG only
file_handler = DebugRotatingFileHandler('tmp/website_DEBUG.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.info('website startup')
app.logger.debug('website startup')

# Register blueprints
from app.mod_projects.views import mod_projects as projects_module
app.register_blueprint(projects_module)

from app import views, models
