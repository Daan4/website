from flask import render_template
from . import mod_todo


@mod_todo.route('/')
def index():
    return render_template('todo.html')
