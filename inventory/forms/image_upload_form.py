from django.forms import (
    ClearableFileInput,
    ImageField,
    Form,
    HiddenInput,
)
from filer.models import Image
from inventory.forms.default_form_text import item_image_help


class ImageUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=True,
        help_text=item_image_help['new_images'])
