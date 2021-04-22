from inventory.views import GenericWizard
from inventory.forms import (
    ChooseTagsForm,
    PickNameForm,
)
from django.contrib import messages
from django.urls import reverse
from inventory.models import (
    Item,
    Subitem,
    Tag
)


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
            self.tags = self.forms[0].cleaned_data['tags']
            self.target_tag = self.forms[0].cleaned_data['tag']
            items_to_merge = Item.objects.filter(
                tags__in=self.tags.exclude(pk=self.target_tag.pk)).exclude(
                tags__pk=self.target_tag.pk)
            self.num_items = len(items_to_merge)
            self.target_tag.items.add(*items_to_merge)
            subitems_to_merge = Subitem.objects.filter(
                tags__in=self.tags.exclude(pk=self.target_tag.pk)).exclude(
                tags__pk=self.target_tag.pk)
            self.num_subitems = len(subitems_to_merge)
            self.target_tag.subitems.add(*subitems_to_merge)
            self.tags.exclude(pk=self.target_tag.pk).delete()

    def finish(self, request):
        messages.success(
            request,
            "Merged %d tags, %d items, %d subitems to %s." % (
                len(self.tags),
                self.num_items,
                self.num_subitems,
                self.target_tag))
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
