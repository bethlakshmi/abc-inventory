from django.forms import ModelForm
from inventory.models import Subitem
from dal import autocomplete


class SubitemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = Subitem
        fields = ['title',
                  'description',
                  'subitem_number',
                  'width',
                  'height',
                  'depth',
                  'tags',
                  'item']
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete'),
            'item': autocomplete.ModelSelect2(
                url='connection-autocomplete')}


class TroupeSubitemForm(SubitemForm):
    class Meta:
        model = Subitem
        fields = ['title',
                  'description',
                  'subitem_number',
                  'width',
                  'height',
                  'depth',
                  'size',
                  'quantity',
                  'tags',
                  'item']
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete'),
            'item': autocomplete.ModelSelect2(
                url='connection-autocomplete')}
