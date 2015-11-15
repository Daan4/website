from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .navigation import MyNavigation as Navigation
from .navigation import NavBarItem as Item
from flaskext.markdown import Markdown
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
nav = Navigation()
module_setup_functions = []


def create_app(config):
    # Flask
    app = Flask(__name__)
    app.config.from_object(config)

    # SQLAlchemy
    db.init_app(app)

    # Flask-Markdown
    Markdown(app)

    # Flask-Navigation
    nav.init_app(app)

    # Create main navigation bar and add Home button.
    nav.Bar('base', [nav.Item('Home', 'index')])

    # Setup modules
    import app.mod_projects as mod_projects
    import app.mod_streams as mod_streams
    import app.mod_auth as mod_auth
    import app.mod_adminpanel as mod_adminpanel
    import app.mod_todo as mod_todo
    for f in module_setup_functions:
        f(app, nav, nav['base'])

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

    return app


def register_module():
    def decorator(f):
        module_setup_functions.append(f)
        return f
    return decorator
