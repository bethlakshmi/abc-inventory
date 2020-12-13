from django.forms import (
    CharField,
    HiddenInput,
    ModelForm,
    ModelChoiceField,
)
from inventory.models import (
    Item,
    ItemImage,
)
from dal import autocomplete
from filer.models.imagemodels import Image


class ImageAssociateForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    filer_image = ModelChoiceField(widget=HiddenInput(),
                                   queryset=Image.objects.all())
    item = ModelChoiceField(
        queryset=Item.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='connection-autocomplete'))

    class Meta:
        model = ItemImage
        fields = [
            'filer_image',
            'item']
