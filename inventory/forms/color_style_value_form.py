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
    style_property = ModelChoiceField(
        widget=HiddenInput(),
        queryset=StyleProperty.objects.filter(value_type='color'))
    value = CharField(
         widget=TextInput(attrs={'data-jscolor': ''}),
        required=False)

    class Meta:
        model = StyleValue
        fields = [
            'style_property',
            'value']
