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
            # Confirm tag1, tag2, ... into <chosen tag selection>
            tag_list = "Confirm merge of tags: "
            for tag in self.tags:
                tag_list = tag_list + tag.name + ', '
            self.current_form_set['confirm_msg'] = (
                "'%s'+document.getElementById('id_tag').options[document." +
                "getElementById('id_tag').selectedIndex].text+'.'") % (
                " into ".join(tag_list.rsplit(", ", 1)))
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
            "Merged %d tags, re-tagged %d items and %d subitems to %s." % (
                len(self.tags),
                self.num_items,
                self.num_subitems,
                self.target_tag))
        return self.return_url

    def setup_forms(self, form, request=None):
        if request:
            if str(form().__class__.__name__) == "ChooseTagsForm":
                return [form(request.POST)]
            else:
                pick_form = form(request.POST)
                pick_form.fields['tag'].queryset = Tag.objects.filter(
                     pk__in=request.POST.getlist("tags"))
                return [pick_form]
        else:
            if str(form().__class__.__name__) == "ChooseTagsForm":
                return [form()]
            else:
                pick_form = form(initial={'tags': self.tags})
                pick_form.fields['tag'].queryset = self.tags
                return [pick_form]
