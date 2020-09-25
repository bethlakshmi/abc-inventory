from django.forms import (
    IntegerField,
    HiddenInput,
    ModelForm,
    NumberInput,
)
from inventory.models import Item
from django.core.exceptions import ValidationError


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
    def clean(self):
        # run the parent validation first
        cleaned_data = super(PhysicalItemForm, self).clean()

        # doing is_complete doesn't work, that executes the pre-existing
        # instance, not the current data

        if cleaned_data.get("date_acquired") and cleaned_data.get(
                "date_deaccession") and cleaned_data.get(
                "date_acquired") > cleaned_data.get("date_deaccession"):
            error = ValidationError((
                'The date acquired cannot be AFTER the date of deaccession' +
                ' - check these dates and try again.'),
                code='invalid')
            self.add_error('date_deaccession', error)
        return cleaned_data
