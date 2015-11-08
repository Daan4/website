from flask_wtf import Form
from app import stream_api
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class StreamConfigurationForm(Form):
    channel = StringField('channel', validators=[DataRequired()])
    add = SubmitField('add')
    remove = SubmitField('remove')