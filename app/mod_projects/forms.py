from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from app.validators import RequiredWhenFieldsHaveData


# Used by mod_adminpanel module to show configuration form in the admin panel.
class EditProjectForm(Form):
    name = StringField('Title', validators=[RequiredWhenFieldsHaveData('add', 'remove')])
    content = TextAreaField('Content')
    add = SubmitField('Add')
    remove = SubmitField('Remove')
    all_projects = SelectField('Projects')
    load = SubmitField('Load')
