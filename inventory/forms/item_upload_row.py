from django.forms import (
    CharField,
    Form,
)
from inventory.forms.default_form_text import item_format_error
from datetime import datetime


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

    def validate_and_format(self, translator):
        is_valid = super(ItemUploadRow, self).is_valid()
        if not is_valid:
            return is_valid
        item_data = {}
        had_error = False
        for key, value in translator.items():
            if len(self.cleaned_data[value].strip()) > 0:
                try:
                    if key in ('width', 'height', 'depth', 'price'):
                        item_data[key] = float(self.cleaned_data[value])
                    elif key in ('date_acquired', 'date_deaccession'):
                        item_data[key] = datetime.strptime(
                            self.cleaned_data[value],
                            '%m/%d/%y')
                    else:
                       item_data[key] = self.cleaned_data[value]
                except:
                    self.add_error(value, item_format_error[key])
                    had_error = True
        if had_error:
            return None
        return item_data
