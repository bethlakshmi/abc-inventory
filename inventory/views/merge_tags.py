from inventory.views import GenericWizard
from inventory.forms import (
    ChooseTagsForm,
    PickNameForm,
)
from django.contrib import messages
from inventory.functions import upload_and_attach
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from django.urls import reverse


class MergeTags(GenericWizard):
    template = 'inventory/generic_wizard.tmpl'
    page_title = 'Merge Tags'
    first_title = 'Pick Tags to Merge'
    second_title = 'Select Tag Name'
    form_sets = {
        -1: {
            'the_form':  None,
            'next_form': ChooseTagsForm,
            'next_title': first_title},
        0: {
            'the_form':  ChooseTagsForm,
            'next_form': PickNameForm,
            'next_title': second_title},
        1: {
            'the_form':  PickNameForm,
            'next_form': None,
            'next_title': None},
    }

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))
        self.return_url = reverse('tags_list', urlconf='inventory.urls')

    def finish_valid_form(self, request):
        if self.forms[0].__class__.__name__ == "ChooseTagsForm":
            self.tags = self.forms[0].cleaned_data['tags']
        else:
            raise Exception("merge here!")

    def finish(self, request):
        messages.success(
            request,
            "Merged %d tags to %s." % (
                len(self.tags),
                self.tag))
        return self.return_url

    def setup_forms(self, form, request=None):
        if request:
            return [form(request.POST)]
        else:
            if str(form().__class__.__name__) == "ChooseTagsForm":
                return [form()]
            else:
                pick_form = PickNameForm(initial={'tags': self.tags})
                pick_form.fields['tag'].queryset = self.tags
                return [pick_form]
