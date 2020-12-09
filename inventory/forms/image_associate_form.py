from django.forms import (
    ClearableFileInput,
    ImageField,
    ModelForm,
    ModelMultipleChoiceField,
    TextInput,
)
from django.forms.widgets import CheckboxSelectMultiple
from inventory.models import ItemImage
from django.utils.safestring import mark_safe
from dal import autocomplete


class ImageAssociateForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = ItemImage
        fields = [
            'filer_image',
            'item']
        widgets = {
            'title': TextInput(attrs={'size': '87'}),
            'item': autocomplete.ModelSelect2(
                url='connection-autocomplete')}
