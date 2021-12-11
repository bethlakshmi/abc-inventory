from django.forms import (
    BooleanField,
    FileField,
    Form,
    HiddenInput,
    IntegerField,
)
from inventory.forms.default_form_text import item_upload_help
from django.core.validators import FileExtensionValidator
from csv import reader
from io import StringIO


class ItemUploadForm(Form):
    required_css_class = 'required'
    error_css_class = 'error'

    step = IntegerField(widget=HiddenInput(), initial=0)
    new_items = FileField(required=True,
                          validators=[FileExtensionValidator(['csv'])])
    has_header = BooleanField(label=item_upload_help['has_header'])

    def check_and_get_data(self):
        csv_file = self.cleaned_data['new_items']
        csv_data = []
        num_cols = 0
        header = None

        # parse and create a data structure
        data_set = csv_file.read().decode('UTF-8')
        io_string = StringIO(data_set)
        csv_reader = reader(io_string, delimiter=',', quotechar='"')
        if self.cleaned_data["has_header"]:
            header = csv_reader.__next__()
            num_cols = len(header)
        for row in csv_reader:
            row[0] = row[0].replace(u'\ufeff', '')
            csv_data += [row]
            if num_cols == 0:
                num_cols = len(row)
            elif num_cols != len(row):
                self.add_error(
                    'new_items',
                    'Irregular number of columns, the delimiter is a ' +
                    'comma (,) and the quote is a double quote ("), ' +
                    'this is likely an encoding problem.  Problem ' +
                    'row: %s' % row)
                return (0, None, None)
        return (num_cols, header, csv_data)
