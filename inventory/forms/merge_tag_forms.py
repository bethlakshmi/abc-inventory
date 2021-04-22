from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    IntegerField,
    Form,
    ModelChoiceField,
    ModelMultipleChoiceField,
)
from inventory.models import Tag


class ChooseTagsForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    required=True,
                                    widget=CheckboxSelectMultiple)
    step = IntegerField(widget=HiddenInput(), initial=0)


class PickNameForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    tag = ModelChoiceField(queryset=Tag.objects.all(),
                           required=True,
                           empty_label=None)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    required=True)
    step = IntegerField(widget=HiddenInput(), initial=1)
