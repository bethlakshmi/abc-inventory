from django.forms import (
    CharField,
    IntegerField,
    HiddenInput,
    ModelForm,
    Textarea,
    TextInput,
)
from inventory.models import Item
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class BasicItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    description = CharField(
        required=False,
        widget=Textarea(attrs={'class': 'user-tiny-mce'}))
    step = IntegerField(widget=HiddenInput(), initial=0)

    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'subject']
        widgets = {
            'title': TextInput(attrs={'size': '82'}),
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete')}


class TroupeBasicItemForm(BasicItemForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'shows',
            'acts',
            'description',
            'category']
        widgets = {
            'shows': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='show-autocomplete'),
                reverse_lazy('show_create', urlconf='inventory.urls'),
                reverse_lazy('show_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])),
            'acts': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='act-autocomplete'),
                reverse_lazy('act_create', urlconf='inventory.urls'),
                reverse_lazy('act_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])),
            'title': TextInput(attrs={'size': '82'}),
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete')}
