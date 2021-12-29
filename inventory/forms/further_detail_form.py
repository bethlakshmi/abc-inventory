from django.forms import (
    HiddenInput,
    ModelForm,
)
from inventory.models import Item
from dal import autocomplete


class FurtherDetailForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Item
        fields = [
            'note',
            'tags',
            'connections']
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete'),
            'connections': autocomplete.ModelSelect2Multiple(
                url='connection-autocomplete')}
