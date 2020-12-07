from django.forms import (
    ClearableFileInput,
    ImageField,
    Form,
    ModelMultipleChoiceField,
)
from django.forms.widgets import CheckboxSelectMultiple
from inventory.models import (
    Item,
    ItemImage,
    UserMessage,
)
from django.utils.safestring import mark_safe
from filer.models import Image
from easy_thumbnails.files import get_thumbnailer
from inventory.forms.default_form_text import item_image_help


class ImageUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

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
