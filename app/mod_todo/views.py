from flask import Blueprint, render_template

mod_todo = Blueprint('todo', __name__, url_prefix='/todo', template_folder='templates')


@mod_todo.route('/')
def index():
    return render_template('todo.html')
