from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


# Used by mod_adminpanel module to show configuration form in the admin panel.
class ConfigForm(Form):
    project = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')
