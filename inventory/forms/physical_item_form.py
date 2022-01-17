from django.forms import (
    CheckboxSelectMultiple,
    DateField,
    HiddenInput,
    ModelForm,
    MultipleChoiceField,
    NumberInput,
)
from inventory.models import Item
from django.core.exceptions import ValidationError
from tempus_dominus.widgets import DatePicker
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy
from inventory.forms.default_form_text import size_options


class PhysicalItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    date_acquired = DateField(required=False, widget=DatePicker(
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
            },
        options={
            'format': "M/D/YYYY",
        }))
    date_deaccession = DateField(required=False, widget=DatePicker(
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
            },
        options={
            'format': "M/D/YYYY",
        }))

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
                   'depth': NumberInput(attrs={'style': 'width: 75px'}),
                   'disposition': autocomplete.ModelSelect2(
                        url='disposition-autocomplete')}


class TroupePhysicalItemForm(PhysicalItemForm):
    sz = MultipleChoiceField(choices=size_options,
                             required=False,
                             widget=CheckboxSelectMultiple())
    class Meta:
        model = Item
        fields = [
            'width',
            'height',
            'depth',
            'size',
            'sz',
            'performers',
            'quantity',
            'disposition',
            'date_acquired',
            'date_deaccession',
            'last_used',
            'price']
        widgets = {
            'width': NumberInput(attrs={'style': 'width: 75px'}),
            'height': NumberInput(attrs={'style': 'width: 75px'}),
            'depth': NumberInput(attrs={'style': 'width: 75px'}),
            'disposition': autocomplete.ModelSelect2(
                url='disposition-autocomplete'),
            'performers': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='performer-autocomplete'),
                reverse_lazy('performer_create', urlconf='inventory.urls'),
                reverse_lazy('performer_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])), }
