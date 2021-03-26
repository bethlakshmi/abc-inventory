from inventory.views import GenericWizard
from inventory.forms import (
    ItemUploadForm,
)
from django.contrib import messages
from inventory.functions import upload_and_attach
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


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
            'next_form': ItemUploadForm,
            'next_title': second_title},
        1: {
            'the_form':  ItemUploadForm,
            'next_form': None,
            'next_title': None},
    }

    def finish_valid_form(self, request):
        files = request.FILES.getlist('new_images')
        self.links = 0
        if len(files) > 0:
            # parse and create a data structure
            # validate that this is a CSV and that all rows have same # columns
            pass
        elif self.forms[0].__class__.__name__ == "ImageAssociateForm":
            # use the selection of mappings to build a bulk create
            # do the create
            pass

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s images.<br>Attached %s images." % (
                self.num_files,
                self.links))
        return self.return_url

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
                return []
