from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db, app
import os.path
app.config['CHANGING_DATABASE'] = True
db.create_all()
