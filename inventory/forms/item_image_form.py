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
)
from django.utils.safestring import mark_safe
from filer.models import Image
from easy_thumbnails.files import get_thumbnailer


class MultiItemImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj.filer_image).get_thumbnail(options).url
        return mark_safe("<img src='%s'/>" % thumb_url)

class MultiImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj).get_thumbnail(options).url
        return mark_safe("<img src='%s'/>" % thumb_url)

class ItemImageForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    current_images = MultiItemImageField(
        widget=CheckboxSelectMultiple,
        queryset=ItemImage.objects.all(),
        required=False)
    imported_images = MultiImageField(
        widget=CheckboxSelectMultiple,
        queryset=Image.objects.filter(itemimage__isnull=True),
        required=False)
    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=False,
    )
    class Meta:
        model = Item
        fields = []
