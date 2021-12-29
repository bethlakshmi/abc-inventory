from django.forms import (
    CharField,
    ModelForm,
    Textarea,
    TextInput
)
from inventory.models import Item
from dal import autocomplete
from django_addanother.widgets import AddAnotherEditSelectedWidgetWrapper
from django.urls import reverse_lazy


class ItemRelatedData(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    title = CharField(disabled=True,
                      label="Title",
                      widget=TextInput(attrs={'size': '100'}))

    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'category',
            'disposition',
            'tags',
            'shows',
            'acts',
            'performers',
            'colors']
        widgets = {
            'colors': autocomplete.ModelSelect2Multiple(
                url='color-autocomplete'),
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
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete'),
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete'),
            'disposition': autocomplete.ModelSelect2(
                url='disposition-autocomplete'),
            'performers': AddAnotherEditSelectedWidgetWrapper(
                autocomplete.ModelSelect2Multiple(
                    url='performer-autocomplete'),
                reverse_lazy('performer_create', urlconf='inventory.urls'),
                reverse_lazy('performer_update',
                             urlconf='inventory.urls',
                             args=['__fk__'])),
            }
