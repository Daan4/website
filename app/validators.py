from wtforms import ValidationError


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
