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


class MultiImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj).get_thumbnail(options).url
        return mark_safe("<img src='%s'/>" % thumb_url)

class ItemImageForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    current_images = MultiImageField(
        widget=CheckboxSelectMultiple(attrs={'style':"display: none;"}),
        queryset=Image.objects.all(),
        required=False)
    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=False,
    )
    class Meta:
        model = Item
        fields = []
