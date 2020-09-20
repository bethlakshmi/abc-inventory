from django.forms import (
    CharField,
    CheckboxSelectMultiple,
    DurationField,
    HiddenInput,
    ModelForm,
    MultipleChoiceField,
    Textarea,
    TextInput,
    URLField,
    URLInput,
)
from inventory.models import Item


class BasicItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    description = CharField(
        required=True,
        widget=Textarea(attrs={'id': 'user-tiny-mce'}))

    subject = CharField(
        required=True,
        widget=Textarea(attrs={'id': 'user-tiny-mce'}))

    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'subject']
