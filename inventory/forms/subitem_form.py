from django.forms import ModelForm
from inventory.models import Subitem
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy

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
                  'performers',
                  'quantity',
                  'tags',
                  'item']
        widgets = {
            'performers': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2(
                    url='performer-autocomplete'),
                reverse_lazy('performer_create', urlconf='inventory.urls'),
                reverse_lazy('performer_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])),
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete'),
            'item': autocomplete.ModelSelect2(
                url='connection-autocomplete')}
