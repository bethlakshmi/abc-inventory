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


class BasicItemForm(ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    description = CharField(
        required=False,
        widget=Textarea(attrs={'id': 'user-tiny-mce'}))
    step = IntegerField(widget=HiddenInput(), initial=0)

    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'category',
            'subject']
        widgets = {
            'title': TextInput(attrs={'size': '87'}),
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete')}
