from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


# Used by mod_adminpanel module to show configuration form in the admin panel.
class ConfigForm(Form):
    project = StringField('project', validators=[DataRequired()])
    content = TextAreaField('project_content', validators=[DataRequired()])
    add = SubmitField('add')
    remove = SubmitField('remove')
