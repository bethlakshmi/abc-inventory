from django.forms import ModelMultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from inventory.forms.default_form_text import item_image_help
from inventory.forms import ImageUploadForm
from filer.models import Image
from inventory.models import UserMessage


class MultiImageField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        other_links = "No Item Links"
        options = {'size': (100, 100), 'crop': False}
        thumb_url = get_thumbnailer(obj).get_thumbnail(options).url
        if obj.itemimage_set.exists():
            other_links = "Linked to:"
            for link in obj.itemimage_set.all():
                other_links = "%s %s;" % (other_links, link.item.title)
        return mark_safe(
            "<img src='%s' title='%s'/>" % (thumb_url, other_links))


class ItemImageForm(ImageUploadForm):
    required_css_class = 'required'
    error_css_class = 'error'

    current_images = MultiImageField(
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
