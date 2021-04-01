from inventory.views import GenericWizard
from inventory.forms import (
    ItemUploadForm,
    ItemUploadMapping,
    ItemUploadRow,
)
from inventory.models import Item
from django.contrib import messages
import csv
import io


class BulkItemUpload(GenericWizard):
    filer_images = []
    template = 'inventory/bulk_item_wizard.tmpl'
    page_title = 'Item Inventory Upload'
    first_title = 'Select File of Items'
    second_title = 'Preview Item Upload & Select Column Mapping'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ItemUploadForm,
            'next_title': first_title,
            'instruction_key': "BULK_FILE_UPLOAD_INSTRUCTIONS"},
        0: {
            'the_form':  ItemUploadForm,
            'next_form': ItemUploadMapping,
            'next_title': second_title,
            'instruction_key': "SETUP_ITEM_UPLOAD_INSTRUCTIONS"},
        1: {
            'the_form':  ItemUploadMapping,
            'next_form': None,
            'next_title': None},
    }
    header = None

    def validate_forms(self):
        if self.forms[0].__class__.__name__ == "ItemUploadForm":
            return super(BulkItemUpload, self).validate_forms()
        elif self.forms[0].__class__.__name__ == "ItemUploadMapping":
            all_valid = True
            self.new_items = []
            translator = {}
            i = 0
            if not self.forms[0].is_valid():
                return False

            while i < self.forms[0].cleaned_data['num_cols']:
                if len(self.forms[0].cleaned_data['header_%d' % i]) > 0:
                    translator[self.forms[0].cleaned_data[
                        'header_%d' % i]] = "cell_%d" % i
                i = i + 1
            for item_form in self.forms[1:]:
                formatted_data = item_form.validate_and_format(translator)
                if formatted_data:
                    self.new_items += [formatted_data]
                else:
                    all_valid = False
            return all_valid

    def finish_valid_form(self, request):
        if self.forms[0].__class__.__name__ == "ItemUploadForm":
            csv_file = request.FILES['new_items']
            self.csv_data = []
            self.num_cols = 0
            # parse and create a data structure
            # validate that this is a CSV and that all rows have same # columns
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            csv_reader = csv.reader(io_string, delimiter=',', quotechar='"')
            if self.forms[0].cleaned_data["has_header"]:
                self.header = csv_reader.__next__()
                self.num_cols = len(self.header)
            for row in csv_reader:
                row[0] = row[0].replace(u'\ufeff', '')
                self.csv_data += [row]
                if self.num_cols == 0:
                    self.num_cols = len(row)
                elif self.num_cols != len(row):
                    messages.error(
                        request,
                        'Irregular number of columns, the delimiter is a ' +
                        'comma (,) and the quote is a double quote ("), ' +
                        'this is likely an encoding problem.  Problem ' +
                        'row: %s' % row)
                    self.csv_data = []
                    break
            self.num_rows = len(self.csv_data)

        elif self.forms[0].__class__.__name__ == "ItemUploadMapping":
            # use the selection of mappings to build a bulk create
            # do the create
            Item.objects.bulk_create([Item(**kv) for kv in self.new_items])
            self.num_rows = len(self.new_items)

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s items." % (
                self.num_rows))
        return self.return_url

    def make_context(self, request):
        context = super(BulkItemUpload, self).make_context(request)
        if str(self.forms[0].__class__.__name__) == "ItemUploadMapping":
            context['special_handling'] = True
        if self.header:
            context['header'] = self.header
        return context

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ItemUploadForm":
                return [form(request.POST, request.FILES)]
            else:
                # set up the choice form based on number of columns.
                if 'num_cols' not in request.POST.keys() or (
                        'num_rows' not in request.POST.keys()):
                    return []
                num_cols = int(request.POST['num_cols'])
                num_rows = int(request.POST['num_rows'])
                forms = [ItemUploadMapping(request.POST,
                                           initial={'num_cols': num_cols})]
                i = 0
                while i < num_rows:
                    forms += [ItemUploadRow(request.POST,
                                            num_cols=num_cols,
                                            prefix=str(i))]
                    i = i + 1
                return forms
        else:
            if str(form().__class__.__name__) == "ItemUploadForm":
                return [form()]
            else:
                # set up the choice form based on number of columns.
                forms = [ItemUploadMapping(initial={
                    'num_cols': self.num_cols,
                    'num_rows': self.num_rows})]
                i = 0
                for row in self.csv_data:
                    forms += [ItemUploadRow(row=row, prefix=str(i))]
                    i = i + 1
                return forms
