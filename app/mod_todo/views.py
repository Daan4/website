from flask import render_template, Blueprint

mod_todo = Blueprint('todo', __name__, url_prefix='/todo', template_folder='templates',
                     static_folder='static')


@mod_todo.route('/')
def index():
    return render_template('todo.html')
