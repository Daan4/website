from app import db, create_app
from werkzeug.utils import ImportStringError

try:
    app = create_app('config.config')
except ImportStringError:
    app = create_app('config.heroku_config')

db.create_all(app=app)
