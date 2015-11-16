from wtforms import *
from flask_wtf import Form
from wtforms.validators import *
from app.validators import *
from app.fields import *


class CreateTodoItemForm(Form):
    todo = TextAreaField('Todo', validators=[DataRequired()])
    category = NonValidatingSelectField('Category')
    priority = NonValidatingSelectField('Priority')
    do_before = DateTimeField('Do before')
    create = SubmitField('Create')


class TodoConfigForm(Form):
    category = StringField('Category', validators=[RequiredWhenFieldsHaveData('create_category', 'delete_category')])
    create_category = SubmitField('Create category')
    delete_category = SubmitField('Delete category')
    priority_name = StringField('Priority name', validators=[RequiredWhenFieldsHaveData('create_priority', 'delete_priority')])
    priority_value = IntegerField('Priority value', validators=[RequiredWhenFieldsHaveData('create_priority'), Optional()])
    create_priority = SubmitField('Create priority')
    delete_priority = SubmitField('Delete priority')
