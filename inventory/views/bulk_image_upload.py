from inventory.views import GenericWizard
from inventory.forms import (
    ImageUploadForm,
    ImageAssociateForm,
    ImageAssociateMetaForm,
)
from django.contrib import messages
from inventory.functions import upload_and_attach
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer


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
    options = {'size': (100, 100), 'crop': False}


    def finish_valid_form(self, request):
        files = request.FILES.getlist('new_images')
        self.links = 0
        self.num_files = len(files)
        if len(files) > 0:
            self.filer_images = upload_and_attach(
                files,
                request.user)
        elif self.forms[0].__class__.__name__ == "ImageAssociateMetaForm":
            self.num_files = self.forms[0].cleaned_data['association_count']
            for form in self.forms:
                if form.__class__.__name__ != "ImageAssociateMetaForm" and (
                        form.cleaned_data['item']):
                    form.save()
                    self.links = self.links + 1

    def finish(self, request):
        messages.success(request, "Uploaded %s Images" % 10)
        return self.return_url

    def setup_forms(self, form, POST=None):
        if POST:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form(POST)]
            else:
                meta_form = ImageAssociateMetaForm(POST)
                if not meta_form.is_valid():
                    # TODO - better error handling here
                    return []
                forms = [meta_form]
                for i in range(0,
                               meta_form.cleaned_data['association_count']+1):
                    association_form = form(POST, prefix=str(i))
                    forms += [association_form]
                return forms
        else:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form()]
            else:
                forms = []
                association_num = 0
                for image in self.filer_images:
                    association_form = form(initial={'filer_image': image},
                                            prefix=str(association_num))
                    thumb_url = get_thumbnailer(image).get_thumbnail(
                        self.options).url
                    association_form.fields['item'].label = mark_safe(
                        "<img src='%s' title='%s'/>" % (thumb_url, image))
                    forms += [association_form]
                    association_num = association_num + 1
                forms += [ImageAssociateMetaForm(
                    initial={'association_count': association_num - 1})]
                return forms

