from wtforms import SelectField


class NonValidatingSelectField(SelectField):
    """ A WTForms SelectField without built-in validation.
    """
    def pre_validate(self, form):
        pass
