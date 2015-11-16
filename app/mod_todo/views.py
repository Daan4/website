from flask import *
from .forms import *
from .models import *
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *
from app.mod_adminpanel.views import register_adminpanel

mod_todo = Blueprint('todo', __name__, url_prefix='/todo', template_folder='templates',
                     static_folder='static')


@mod_todo.route('/', methods=['GET', 'POST'])
def index():
    form = CreateTodoItemForm()
    form.category.choices = [(c.id, c.category) for c in TodoCategory.query.all()]
    form.priority.choices = [(p.id, p.name) for p in TodoPriority.query.all()]
    if form.validate_on_submit():
        if form.create.data:
            todo = form.todo.data
            category = form.category.data
            priority = form.priority.data
            do_before = form.do_before.data
            add_todo_item(todo, category, priority, do_before)
            flash('New todo item created')
    return render_template('todo.html', form=form)


def add_todo_item(todo, category_id, priority_id, do_before):
    pass


def close_todo_item(todo_id):
    pass


def remove_todo_item(todo_id):
    pass


@register_adminpanel(mod_todo.name)
def do_adminpanel_logic():
    form = TodoConfigForm()
    if form.validate_on_submit():
        category = form.category.data
        priority_name = form.priority_name.data
        priority_value = form.priority_value.data
        if form.create_category.data:
            TodoCategory.create('Category {} added'.format(category),
                                'Category {} already exists'.format(category),
                                category=category)
        elif form.delete_category.data:
            TodoCategory.delete('Category {} deleted'.format(category),
                                'Category {} doesn\'t exist'.format(category),
                                category=category)
        elif form.create_priority.data:
            TodoPriority.create('Priority {} added'.format(priority_name),
                                'Priority {} already exists'.format(priority_name),
                                name=priority_name, priority=priority_value)
        elif form.delete_priority.data:
            TodoPriority.delete('Priority {} deleted'.format(priority_name),
                                'Priority {} doesn\'t exist'.format(priority_name),
                                name=priority_name)
    return render_template('todo_config.html', form=form, title='Admin Panel - ToDo')
