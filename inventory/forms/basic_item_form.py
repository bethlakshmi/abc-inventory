from django.forms import (
    CharField,
    IntegerField,
    HiddenInput,
    ModelForm,
    Textarea,
)
from inventory.models import Item


class BasicItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'


    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'subject']
