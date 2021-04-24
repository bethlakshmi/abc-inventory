from django.forms import (
    CheckboxSelectMultiple,
    HiddenInput,
    IntegerField,
    Form,
    ModelChoiceField,
    ModelMultipleChoiceField,
    MultipleHiddenInput,
)
from inventory.models import Category
from inventory.forms import validate_two_choices


class ChooseCategoryForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    categories = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                    required=True,
                                    widget=CheckboxSelectMultiple,
                                    validators=[validate_two_choices])
    step = IntegerField(widget=HiddenInput(), initial=0)


class PickCategoryNameForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    category = ModelChoiceField(queryset=Category.objects.all(),
                           required=True,
                           empty_label=None)
    categories = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                    required=True,
                                    widget=MultipleHiddenInput(),
                                    validators=[validate_two_choices])
    step = IntegerField(widget=HiddenInput(), initial=1)
