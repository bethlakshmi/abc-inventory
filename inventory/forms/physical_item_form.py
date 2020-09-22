from django.forms import (
    IntegerField,
    HiddenInput,
    ModelForm,
    NumberInput,
)
from inventory.models import Item


class PhysicalItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)

    class Meta:
        model = Item
        fields = [
            'width',
            'height',
            'depth',
            'disposition',
            'year',
            'date_acquired',
            'date_deaccession',
            'price']
        widgets = {'width': NumberInput(attrs={'style': 'width: 75px'}),
                   'height': NumberInput(attrs={'style': 'width: 75px'}),
                   'depth': NumberInput(attrs={'style': 'width: 75px'})}
