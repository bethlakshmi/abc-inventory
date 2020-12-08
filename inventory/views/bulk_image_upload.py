from inventory.views import GenericWizard
from inventory.forms import (
    ImageUploadForm,
    ImageAssociateForm,
)
from django.contrib import messages
from inventory.functions import upload_and_attach


class BulkImageUpload(GenericWizard):
    filer_images = []
    template = 'inventory/image_upload_wizard.tmpl'
    page_title = 'Image Upload'
    first_title = 'Select Images to Upload'
    second_title = 'Connect Images to Items'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ImageUploadForm,
            'next_title': first_title},
        0: {
            'the_form':  ImageUploadForm,
            'next_form': ImageAssociateForm,
            'next_title': second_title},
        1: {
            'the_form':  ImageAssociateForm,
            'next_form': None,
            'next_title': None},
    }

    def finish_valid_form(self, request):
        files = request.FILES.getlist('new_images')
        if len(files) > 0:
            self.filer_images = upload_and_attach(
                files,
                request.user)

    def finish(self, request):
        messages.success(request, "Uploaded %s Images" % 10)
        return self.return_url

    def setup_form(self, form, POST=None):
        if POST:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return form(POST)
            else:
                raise Exception(str(form.__class__.__name__))
        else:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return form()
            else:
                forms = []
                for image in self.filer_images:
                    forms += [form(initial={'filer_image': image},
                                   prefix=str(image.pk))]
                return forms

