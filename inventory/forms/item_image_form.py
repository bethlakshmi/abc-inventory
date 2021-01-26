from django.forms import (
    ClearableFileInput,
    ImageField,
    Form,
)
from django.forms.widgets import CheckboxSelectMultiple
from inventory.forms import ThumbnailImageField
from inventory.forms.default_form_text import item_image_help
from filer.models import Image
from inventory.models import UserMessage


class ItemImageForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    current_images = ThumbnailImageField(
        widget=CheckboxSelectMultiple(attrs={'style': "display: none;"}),
        queryset=Image.objects.all(),
        required=False,
        help_text=UserMessage.objects.get_or_create(
                view="ItemImageForm",
                code="CURRENT_IMAGE_INSTRUCTIONS",
                defaults={
                    'summary': "Current Image Help text",
                    'description': item_image_help['current_images']}
                )[0].description)

    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=False,
        help_text=UserMessage.objects.get_or_create(
                view="ItemImageForm",
                code="NEW_IMAGE_INSTRUCTIONS",
                defaults={
                    'summary': "New Image Help text",
                    'description': item_image_help['new_images']}
                )[0].description)
