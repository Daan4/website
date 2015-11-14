from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


# Used by mod_adminpanel module to show configuration form in the admin panel.
class ConfigForm(Form):
    name = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    add = SubmitField('Add')
    remove = SubmitField('Remove')
    edit = SubmitField('Edit')


class LoadProjectForm(Form):
    projects = SelectField('Projects')
    edit = SubmitField('Edit')
