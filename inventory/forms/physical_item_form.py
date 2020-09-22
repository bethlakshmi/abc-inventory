from django.forms import (
    CharField,
    IntegerField,
    HiddenInput,
    ModelForm,
    Textarea,
    TextInput,
)
from inventory.models import Item


class PhysicalItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)

    class Meta:
        model = Item
        fields = [
            'height',
            'width',
            'depth',
            'disposition',
            'year',
            'date_acquired',
            'price']