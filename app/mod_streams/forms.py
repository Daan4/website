from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Used by mod_adminpanel module to show configuration form in the admin panel.
class ConfigForm(Form):
    channel = StringField('Twitch channel(s)', validators=[DataRequired()])
    add = SubmitField('Add')
    remove = SubmitField('Remove')
