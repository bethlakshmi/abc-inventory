from django.forms import (
    CharField,
    ModelForm,
    Textarea,
)
from inventory.models import ItemText
from inventory.forms.default_form_text import item_text_help
from inventory.models import UserMessage


class LabelForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    text = CharField(
        help_text=item_text_help,
        required=False,
        widget=Textarea(attrs={'class': 'user-tiny-mce'}))

    class Meta:
        model = ItemText
        fields = ['text', ]
