from django.forms import (
    DateField,
    ModelForm,
)
from inventory.models import Act
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy
from tempus_dominus.widgets import DatePicker
from inventory.forms.default_form_text import out_of_order_error
from django.core.exceptions import ValidationError


class ActForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    first_performed = DateField(required=False, widget=DatePicker(
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
            },
        options={
            'format': "M/D/YYYY",
        }))
    last_performed = DateField(required=False, widget=DatePicker(
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
            },
        options={
            'format': "M/D/YYYY",
        }))

    def clean(self):
        # run the parent validation first
        cleaned_data = super(ActForm, self).clean()

        # doing is_complete doesn't work, that executes the pre-existing
        # instance, not the current data

        if cleaned_data.get("first_performed") and cleaned_data.get(
                "last_performed") and cleaned_data.get(
                "first_performed") > cleaned_data.get("last_performed"):
            error = ValidationError(out_of_order_error, code='invalid')
            self.add_error('last_performed', error)
        return cleaned_data

    class Meta:
        model = Act
        fields = ['title',
                  'performers',
                  'shows',
                  'song',
                  'song_artist',
                  'notes',
                  'first_performed',
                  'last_performed']
        widgets = {
            'performers': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='performer-autocomplete'),
                reverse_lazy('performer_create', urlconf='inventory.urls'),
                reverse_lazy('performer_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])),
            'shows': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='show-autocomplete'),
                reverse_lazy('show_create', urlconf='inventory.urls'),
                reverse_lazy('show_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])), }
