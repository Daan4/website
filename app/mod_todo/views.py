from flask import *
from .forms import *
from .models import *
from app.mod_adminpanel.views import register_adminpanel
from flask_login import login_required

mod_todo = Blueprint('todo', __name__, url_prefix='/todo', template_folder='templates',
                     static_folder='static')


@mod_todo.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Check for items to delete and complete, and then delete and complete them.
    ids_to_delete = request.args.get('delete')
    if ids_to_delete:
        for id_ in ids_to_delete.split(','):
            Todo.delete(id=id_)
    ids_to_complete = request.args.get('done')
    if ids_to_complete:
        for id_ in ids_to_complete.split(','):
            todo = Todo.query.filter_by(id=id_).first()
            if isinstance(todo, Todo):
                todo.complete()
    form = CreateTodoItemForm()
    form.category.choices = [(c.id, c.category) for c in TodoCategory.query.all()]
    form.priority.choices = [(p.id, p.name) for p in TodoPriority.query.all()]
    if form.validate_on_submit():
        if form.create.data:
            todo = form.todo.data
            category = form.category.data
            priority = form.priority.data
            do_before = form.do_before.data
            Todo.create('New todo item added',
                        todo=todo,
                        category_id=category,
                        priority_id=priority,
                        do_before=do_before)
    return render_template('todo.html', form=form, todo_items=Todo.query.order_by(Todo.id).all())


@register_adminpanel(mod_todo.name)
def do_adminpanel_logic():
    form = TodoConfigForm()
    if form.validate_on_submit():
        category = form.category.data
        priority_name = form.priority_name.data
        priority_value = form.priority_value.data
        if form.create_category.data:
            TodoCategory.create('Category {} added'.format(category),
                                'Failed: Category {} already exists'.format(category),
                                category=category)
        elif form.delete_category.data:
            TodoCategory.delete('Category {} deleted'.format(category),
                                'Failed: Category {} doesn\'t exist'.format(category),
                                'Failed: Category {} is still in use by some todo items'.format(category),
                                category=category)
        elif form.create_priority.data:
            TodoPriority.create('Priority {} added'.format(priority_name),
                                'Failed: Priority {} already exists'.format(priority_name),
                                name=priority_name, priority=priority_value)
        elif form.delete_priority.data:
            TodoPriority.delete('Priority {} deleted'.format(priority_name),
                                'Failed: Priority {} doesn\'t exist'.format(priority_name),
                                'Failed: Priority {} is still in use by some todo items'.format(priority_name),
                                name=priority_name)
    return render_template('todo_config.html', form=form, title='Admin Panel - ToDo')
