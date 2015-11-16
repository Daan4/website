from wtforms import *
from app.validators import RequiredWhenFieldsHaveData
from app.fields import NonValidatingSelectField


# Used by mod_adminpanel module to show configuration form in the admin panel.
class EditProjectForm(Form):
    name = StringField('Title', validators=[RequiredWhenFieldsHaveData('add', 'remove')])
    content = TextAreaField('Content')
    add = SubmitField('Add')
    remove = SubmitField('Remove')
    all_projects = NonValidatingSelectField('Projects')
    load = SubmitField('Load')
