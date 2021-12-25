from django.forms import (
    ChoiceField,
    Form,
    HiddenInput,
    IntegerField,
)
from inventory.forms.default_form_text import (
    header_choices,
    museum_header_choices,
    troupe_header_choices,
)
from django.core.exceptions import ValidationError
from django.conf import settings


class ItemUploadMapping(Form):
    required_css_class = 'required'
    error_css_class = 'error'
    step = IntegerField(widget=HiddenInput(), initial=1)
    num_rows = IntegerField(widget=HiddenInput(), required=True)
    num_cols = IntegerField(widget=HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        num_cols = 0
        if 'initial' in kwargs and 'num_cols' in kwargs.get('initial'):
            num_cols = kwargs.get('initial')['num_cols']
        super(ItemUploadMapping, self).__init__(*args, **kwargs)
        i = 0
        full_header_choices = header_choices
        if settings.INVENTORY_MODE == "troupe":
            full_header_choices = header_choices + troupe_header_choices
        elif settings.INVENTORY_MODE == "museum":
            full_header_choices = header_choices + museum_header_choices
        while i < num_cols:
            self.fields['header_%s' % i] = ChoiceField(
                choices=full_header_choices,
                required=False)
            i = i + 1

    def clean(self):
        cleaned_data = super().clean()
        found_title = False
        for key, value in cleaned_data.items():
            if value == "title":
                found_title = True
        if not found_title:
            raise ValidationError(
                    "One column must be labeled as the title."
                )
