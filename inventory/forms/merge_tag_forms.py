from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    Form,
    ModelChoiceField,
    ModelMultipleChoiceField,
    MultipleHiddenInput,
)
from inventory.models import Tag
from inventory.forms import validate_two_choices


class ChooseTagsForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    required=True,
                                    widget=CheckboxSelectMultiple,
                                    validators=[validate_two_choices])


class PickTagNameForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    tag = ModelChoiceField(queryset=Tag.objects.all(),
                           required=True,
                           empty_label=None)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                    required=True,
                                    widget=MultipleHiddenInput(),
                                    validators=[validate_two_choices])
