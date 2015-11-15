from flask import Blueprint

mod_todo = None

def setup_module(app, nav, nav_bar):
    # Register blueprint
    global mod_todo
    mod_todo = Blueprint('todo', __name__, url_prefix='/todo', template_folder='templates')
    app.register_blueprint(mod_todo)
    # Setup main menu bar items
    nav_bar.items.append(nav.Item('ToDo', 'todo.index'))
