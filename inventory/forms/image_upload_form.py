from django.forms import (
    ClearableFileInput,
    ImageField,
    IntegerField,
    Form,
    HiddenInput,
)
from inventory.models import UserMessage
from filer.models import Image
from inventory.forms.default_form_text import item_image_help


class ImageUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=True,
        help_text=UserMessage.objects.get_or_create(
                view="ImageUploadForm",
                code="NEW_IMAGE_INSTRUCTIONS",
                defaults={
                    'summary': "New Image Help text",
                    'description': item_image_help['new_images']}
                )[0].description)
    step = IntegerField(widget=HiddenInput(), initial=0)
