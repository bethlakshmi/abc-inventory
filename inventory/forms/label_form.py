from django.forms import (
    CharField,
    ModelForm,
    Textarea,
)
from inventory.models import ItemText


class LabelForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    text = CharField(
        required=False,
        widget=Textarea(attrs={'class': 'user-tiny-mce'}))

    class Meta:
        model = ItemText
        fields = ['text', ]
