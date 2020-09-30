from app import db, create_app
app = create_app('config.config')
db.create_all(app=app)
