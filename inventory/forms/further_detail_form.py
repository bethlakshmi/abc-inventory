from django.forms import (
    IntegerField,
    HiddenInput,
    ModelForm,
)
from inventory.models import Item


class FurtherDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=2)

    class Meta:
        model = Item
        fields = [
            'note',
            'tags',
            'connections']
