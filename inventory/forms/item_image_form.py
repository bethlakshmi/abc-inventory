from django.forms import (
    ClearableFileInput,
    ImageField,
    Form,
    ModelMultipleChoiceField
)
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from django.db.models import Count
from inventory.forms.default_form_text import item_image_help
from filer.models import Image


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


class ItemImageForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    delete_images = ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple(),
        queryset=Image.objects.all(),
        required=False)

    current_images = MultiImageField(
        widget=CheckboxSelectMultiple(attrs={'style': "display: none;"}),
        queryset=Image.objects.all(),
        required=False,
        help_text=item_image_help['current_images'])

    unattached_images = MultiImageField(
        widget=CheckboxSelectMultiple(attrs={'style': "display: none;"}),
        queryset=Image.objects.annotate(
            links=Count('itemimage')).filter(links=0),
        required=False,
        help_text=item_image_help['unattached_images'])

    other_images = MultiImageField(
        widget=CheckboxSelectMultiple(attrs={'style': "display: none;"}),
        queryset=Image.objects.annotate(
            links=Count('itemimage')).exclude(links=0),
        required=False,
        help_text=item_image_help['linked_images'])

    new_images = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
        required=False,
        help_text=item_image_help['new_images'])
