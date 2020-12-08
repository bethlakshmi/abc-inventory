from django.forms import (
    ClearableFileInput,
    ImageField,
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.widgets import CheckboxSelectMultiple
from inventory.models import ItemImage
from django.utils.safestring import mark_safe
from filer.models import Image
from easy_thumbnails.files import get_thumbnailer
from inventory.forms.default_form_text import item_image_help


class ImageAssociateForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = ItemImage
        fields = [
            'item',
            'filer_image']
