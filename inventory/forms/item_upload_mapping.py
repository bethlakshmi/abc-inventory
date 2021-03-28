from django.forms import (
    ChoiceField,
    Form,
    HiddenInput,
    IntegerField,
)
from inventory.forms.default_form_text import header_choices


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
        while i < num_cols:
            self.fields['header_%s' % i] = ChoiceField(choices=header_choices,
                                                       required=False)
            i = i + 1
