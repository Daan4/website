from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectMultipleField
from app.validators import RequiredWhenFieldsHaveData


# Used by mod_adminpanel module to show configuration form in the admin panel.
class ConfigForm(Form):
    channel = StringField('Twitch channel(s)', validators=[RequiredWhenFieldsHaveData('add', 'remove')])
    add = SubmitField('Add')
    remove = SubmitField('Remove')
    all_channels = SelectMultipleField('Channels')
    load = SubmitField('Load')
