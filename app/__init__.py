from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .navigation import MyNavigation as Navigation
from .navigation import NavBarItem as Item
from flaskext.markdown import Markdown

# Flask
app = Flask(__name__)
app.config.from_object('config')

# SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

# Flask-Markdown
Markdown(app)

# Flask-Navigation
nav = Navigation(app)
# Create main navigation bar and add Home button.
nav.Bar('base', [nav.Item('Home', 'index')])


# Register module blueprints
from app.mod_projects.views import mod_projects as projects_blueprint
from app.mod_streams.views import mod_streams as streams_blueprint
from app.mod_adminpanel.views import mod_adminpanel as adminpanel_blueprint
from app.mod_auth.views import mod_auth as auth_blueprint
app.register_blueprint(projects_blueprint)
app.register_blueprint(streams_blueprint)
app.register_blueprint(adminpanel_blueprint)
app.register_blueprint(auth_blueprint)

# Setup modules
nav_bar = nav['base']
import app.mod_projects as projects_module
import app.mod_streams as streams_module
import app.mod_adminpanel as adminpanel_module
import app.mod_auth as auth_module
projects_module.setup_module(nav, nav_bar)
streams_module.setup_module(nav, nav_bar)
adminpanel_module.setup_module(app, nav, nav_bar)
auth_module.setup_module(nav, nav_bar)

# Setup error handling
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

from app import views, models
