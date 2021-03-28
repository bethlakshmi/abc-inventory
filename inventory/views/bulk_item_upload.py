from inventory.views import GenericWizard
from inventory.forms import (
    ItemUploadForm,
    ItemUploadMapping,
)
from django.contrib import messages
import csv, io


class BulkItemUpload(GenericWizard):
    filer_images = []
    template = 'inventory/generic_wizard.tmpl'
    page_title = 'Item Inventory Upload'
    first_title = 'Select File of Items'
    second_title = 'Map File to Image Fields'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ItemUploadForm,
            'next_title': first_title},
        0: {
            'the_form':  ItemUploadForm,
            'next_form': ItemUploadMapping,
            'next_title': second_title},
        1: {
            'the_form':  ItemUploadMapping,
            'next_form': None,
            'next_title': None},
    }
    header = None

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
            csv_reader = csv.reader(io_string, delimiter=',', quotechar="|")
            if self.forms[0].cleaned_data["has_header"]:
                self.header = csv_reader.__next__()
                self.num_cols = len(self.header)
            for row in csv_reader:
                self.csv_data += [row]
                if self.num_cols == 0:
                    self.num_cols = len(row)
                elif self.num_cols != len(row):
                    messages.error(request, 'Irregular number of columns')
                    self.csv_data = []
                    break
            self.num_rows = len(self.csv_data)

        elif self.forms[0].__class__.__name__ == "ItemUploadMapping":
            # use the selection of mappings to build a bulk create
            # do the create
            pass

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s items." % (
                self.num_rows))
        return self.return_url

    def make_context(self, request):
        context = super(BulkItemUpload, self).make_context(request)
        if str(self.forms[0].__class__.__name__) == "PhysicalItemForm":
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
                return []
        else:
            if str(form().__class__.__name__) == "ItemUploadForm":
                return [form()]
            else:
                # set up the choice form based on number of columns.
                forms = [ItemUploadMapping(initial={
                    'num_cols': self.num_cols,
                    'num_rows': self.num_rows})]
                return forms
