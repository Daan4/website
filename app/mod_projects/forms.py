from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, SelectField, ValidationError


# Validator which validates if a field has data when other fields have data.
class RequiredWhenFieldsHaveData:
    def __init__(self, *fields, message=None):
        self.fields = fields
        self.message = message if message else "Field required"

    def __call__(self, form, field):
        for f in self.fields:
            if eval('form.{}.data'.format(f)):
                if field.data == '':
                    raise ValidationError(self.message)
                break


# Used by mod_adminpanel module to show configuration form in the admin panel.
class EditProjectForm(Form):
    name = StringField('Title', validators=[RequiredWhenFieldsHaveData('add', 'remove')])
    content = TextAreaField('Content')
    add = SubmitField('Add')
    remove = SubmitField('Remove')
    projects = SelectField('Projects')
    load = SubmitField('Load')
