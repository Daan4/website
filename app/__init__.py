from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .navigation import MyNavigation as Navigation
from .navigation import NavBarItem as Item
from flaskext.markdown import Markdown
import logging
import importlib
from logging.handlers import RotatingFileHandler

# Flask
app = Flask(__name__)
app.config.from_object('config')

# SQLAlchemy
db = SQLAlchemy(app)

# Flask-Markdown
Markdown(app)

# Flask-Navigation
nav = Navigation(app)
# Create main navigation bar and add Home button.
nav.Bar('base', [nav.Item('Home', 'index')])

# Setup modules
# The order of calling setup_module determines the order of the main navigation bar items.
nav_bar = nav['base']
import app.mod_projects as projects_module
import app.mod_streams as streams_module
import app.mod_adminpanel as adminpanel_module
import app.mod_auth as auth_module
import app.mod_todo as todo_module
modules = [projects_module, streams_module, adminpanel_module, auth_module, todo_module]
for module in modules:
    module.setup_module(app, nav, nav_bar)

# Setup error handling
# if not app.debug:
#     # Via email
#     from logging.handlers import SMTPHandler
#     credentials = None
#     if MAIL_USERNAME or MAIL_PASSWORD:
#         credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#     mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'www.daanlubbers.nl failure', credentials)
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)
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

from app import views, models
from app.mod_projects import views, models
from app.mod_streams import views, models
from app.mod_auth import views, models
from app.mod_adminpanel import views
from app.mod_todo import views, models
