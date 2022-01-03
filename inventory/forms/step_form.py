from django.forms import (
    HiddenInput,
    Form,
    IntegerField,
)


class StepForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)
