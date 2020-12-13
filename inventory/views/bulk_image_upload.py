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
    template = 'inventory/generic_wizard.tmpl'
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
        if len(files) > 0:
            self.num_files = len(files)
            self.filer_images = upload_and_attach(
                files,
                request.user)
        elif self.forms[0].__class__.__name__ == "ImageAssociateForm":
            for form in self.forms:
                if form.__class__.__name__ != "ImageAssociateMetaForm" and (
                        form.cleaned_data['item']):
                    form.save()
                    self.links = self.links + 1

    def finish(self, request):
        messages.success(
            request,
            "Uploaded %s images.<br>Attached %s images." % (
                self.num_files,
                self.links))
        return self.return_url

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form(request.POST, request.FILES)]
            else:
                meta_form = ImageAssociateMetaForm(request.POST)
                if not meta_form.is_valid():
                    return []
                self.num_files = meta_form.cleaned_data['association_count']
                forms = []
                for i in range(0, self.num_files):
                    association_form = form(request.POST,
                                            prefix=str(i),
                                            label_suffix='')
                    if association_form.is_valid():
                        image = association_form.cleaned_data['filer_image']
                        thumb_url = get_thumbnailer(image).get_thumbnail(
                            self.options).url
                        association_form.fields['item'].label = mark_safe(
                            "<img src='%s' title='%s'/>" % (thumb_url, image))
                    forms += [association_form]
                forms += [meta_form]
                return forms
        else:
            if str(form().__class__.__name__) == "ImageUploadForm":
                return [form()]
            else:
                forms = []
                association_num = 0
                for image in self.filer_images:
                    association_form = form(initial={'filer_image': image},
                                            prefix=str(association_num),
                                            label_suffix='')
                    thumb_url = get_thumbnailer(image).get_thumbnail(
                        self.options).url
                    association_form.fields['item'].label = mark_safe(
                        "<img src='%s' title='%s'/>" % (thumb_url, image))
                    forms += [association_form]
                    association_num = association_num + 1
                forms += [ImageAssociateMetaForm(
                    initial={'association_count': association_num})]
                return forms
