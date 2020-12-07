from inventory.views import GenericWizard
from inventory.forms import (
    BasicItemForm,
    FurtherDetailForm,
    PhysicalItemForm,
)
from django.contrib import messages
from django.forms import (
    IntegerField,
    HiddenInput,
)


class BulkImageUpload(GenericWizard):
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Image Upload'
    first_title = 'Select Images to Upload'
    second_title = 'Connect Images to Items'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': BasicItemForm,
            'next_title': first_title},
        0: {
            'the_form':  BasicItemForm,
            'next_form': PhysicalItemForm,
            'next_title': second_title},
        1: {
            'the_form':  PhysicalItemForm,
            'next_form': None,
            'next_title': None},
    }

    def finish_valid_form(self):
        pass

    def finish(self, request):
        messages.success(request, "Uploaded %s Images" % 10)
        return self.return_url

    def setup_form(self, form, POST=None):
        if POST:
            return form(POST)
        else:
            return form()
