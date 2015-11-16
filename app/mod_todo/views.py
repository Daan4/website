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
            create_todo_category(category)
        elif form.delete_category.data:
            delete_todo_category(category)
        elif form.create_priority.data:
            create_todo_priority(priority_name, priority_value)
        elif form.delete_priority.data:
            delete_todo_priority(priority_name)
    return render_template('todo_config.html', form=form, title='Admin Panel - ToDo')


def create_todo_category(category):
    new_category = TodoCategory(category=category)
    try:
        db.session.add(new_category)
        db.session.commit()
        flash('Category {} added'.format(category))
    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        flash('Category {} already exists'.format(category))


def delete_todo_category(category):
    existing_category = TodoCategory.query.filter_by(category=category).first()
    try:
        db.session.delete(existing_category)
        db.session.commit()
        flash('Category {} removed'.format(category))
    except UnmappedInstanceError:
        db.session.rollback()
        flash('Category {} doesn\'t exist'.format(category))


def create_todo_priority(name, value):
    new_priority = TodoPriority(name=name, priority=value)
    try:
        db.session.add(new_priority)
        db.session.commit()
        flash('Priority {} added'.format(name))
    except (IntegrityError, InvalidRequestError):
        db.session.rollback()
        flash('Priority {} already exists'.format(name))


def delete_todo_priority(name):
    existing_priority = TodoPriority.query.filter_by(name=name).first()
    try:
        db.session.delete(existing_priority)
        db.session.commit()
        flash('Priority {} removed'.format(name))
    except UnmappedInstanceError:
        db.session.rollback()
        flash('Priority {} doesn\'t exist'.format(name))
