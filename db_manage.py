from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# script parameters
# db init : creates migrations folder
# db migrate : create migration
# db upgrade [<revision>] : upgrade database to revision
# db downgrade [<revision>] : downgrade database to revision

app.config['CHANGING_DATABASE'] = True

# Flask-Migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
