from django.forms import (
    CheckboxSelectMultiple,
    ModelForm,
    MultipleChoiceField,
)
from inventory.models import Item
from inventory.forms.default_form_text import size_options
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


class SizeSetForm(ModelForm):
    options = {'size': (200, 200), 'crop': False}
    required_css_class = 'required'
    error_css_class = 'error'
    sz = MultipleChoiceField(choices=size_options,
                             required=False,
                             widget=CheckboxSelectMultiple(
                                attrs={'class': 'no_bullet_list'}))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            my_instance = kwargs.get('instance')
            initial = None
            if my_instance.sz and len(my_instance.sz.strip()) > 0:
                kwargs['initial'] = {'sz': eval(my_instance.sz)}
        super(SizeSetForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['size'].label = my_instance.title
            if my_instance.has_image():
                if my_instance.main_image():
                    image = my_instance.main_image()
                else:
                    image = my_instance.images.first()
                image = my_instance.images.first()
                thumb_url = get_thumbnailer(image.filer_image).get_thumbnail(
                    self.options).url
                self.fields['size'].label = mark_safe(
                    "%s<br><img src='%s'/>" % (
                        my_instance.title,
                        thumb_url))

    class Meta:
        model = Item
        fields = ['size', 'sz']
