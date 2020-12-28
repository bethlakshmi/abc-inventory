from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    ModelChoiceField,
    TextInput,
)
from inventory.models import (
    StyleProperty,
    StyleValue,
)
from dal import autocomplete


class ColorStyleValueForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    value = CharField(widget=TextInput(attrs={'data-jscolor': ''}))

    class Meta:
        model = StyleValue
        fields = ['value']
