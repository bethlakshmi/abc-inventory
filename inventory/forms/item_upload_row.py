from django.forms import (
    CharField,
    Form,
)
from inventory.forms.default_form_text import header_choices


class ItemUploadRow(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        row = []
        num_cols = None
        if 'row' in kwargs:
            row = kwargs.pop('row')
        elif 'num_cols' in kwargs:
            num_cols = kwargs.pop('num_cols')
        super(ItemUploadRow, self).__init__(*args, **kwargs)
        i = 0
        if len(row) > 0:
            for item in row:
                self.fields['cell_%s' % i] = CharField(initial=item,
                                                       required=False)
                i = i + 1
        else:
            while i < num_cols:
                self.fields['cell_%s' % i] = CharField(required=False)
                i = i + 1
