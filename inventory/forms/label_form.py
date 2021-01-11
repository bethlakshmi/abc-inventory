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
        help_text=UserMessage.objects.get_or_create(
                view="LabelForm",
                code="ITEM_TEXT_INSTRUCTIONS",
                defaults={
                    'summary': "Item Help Text",
                    'description': item_text_help}
                )[0].description,
        required=False,
        widget=Textarea(attrs={'class': 'user-tiny-mce'}))

    class Meta:
        model = ItemText
        fields = ['text', ]
