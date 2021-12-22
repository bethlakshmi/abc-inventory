from django.shortcuts import get_object_or_404
from inventory.views import GenericWizard
from django.urls import reverse
from inventory.models import Item
from inventory.forms import (
    BasicItemForm,
    FurtherDetailForm,
    LabelForm,
    PhysicalItemForm,
    TroupeBasicItemForm,
    TroupePhysicalItemForm,
)
from django.contrib import messages
from django.forms import (
    IntegerField,
    HiddenInput,
)
from django.conf import settings


class MakeItemWizard(GenericWizard):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Create New Item'
    first_title = 'The Basics'
    second_title = 'Physical Information'
    third_title = 'Further Details'
    item = None
    new_label = None
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
            'next_form': FurtherDetailForm,
            'next_title': third_title},
        2: {
            'the_form':  FurtherDetailForm,
            'next_form': None,
            'next_title': None},
    }

    def groundwork(self, request, args, kwargs):
        if settings.INVENTORY_MODE == "troupe":
            self.form_sets[-1]['next_form'] = TroupeBasicItemForm
            self.form_sets[0]['the_form'] = TroupeBasicItemForm
            self.form_sets[0]['next_form'] = TroupePhysicalItemForm
            self.form_sets[1]['the_form'] = TroupePhysicalItemForm

        redirect = super(MakeItemWizard, self).groundwork(
            request,
            args,
            kwargs)
        self.item = None
        if "item_id" in kwargs:
            self.page_title = 'Edit Item'
            item_id = kwargs.get("item_id")
            self.item = get_object_or_404(Item, id=item_id)
        elif request.POST and request.POST.get("item_id", False):
            self.item = get_object_or_404(Item,
                                          id=int(request.POST.get("item_id")))

    def make_context(self, request):
        context = super(MakeItemWizard, self).make_context(request)
        title = "Creating New Item"
        if self.item:
            title = self.item.title
        context['title'] = title
        if "PhysicalItemForm" in str(self.forms[0].__class__.__name__):
            context['special_handling'] = True
        if str(self.forms[0].__class__.__name__) == "FurtherDetailForm":
            if settings.INVENTORY_MODE == "museum":
                context['add'] = True
            context['images'] = True
        return context

    def finish_valid_form(self, request):
        self.item = self.forms[0].save()
        if self.forms[0].__class__.__name__ == "FurtherDetailForm" and (
                settings.INVENTORY_MODE == "museum"):
            for form in self.forms[1:-1]:
                if len(form.cleaned_data["text"]) == 0:
                    label = form.save(commit=False)
                    label.delete()
                    messages.success(
                        request,
                        "Deleted a text item")
                else:
                    form.save()
            if self.forms[-1].cleaned_data["text"] and len(
                    self.forms[-1].cleaned_data["text"]):
                self.new_label = self.forms[-1].save(commit=False)
                self.new_label.item = self.item
                self.new_label.save()
                if 'add' in list(request.POST.keys()):
                    messages.success(
                        request,
                        "Created new text: %s" % self.new_label.text)

    def finish(self, request):
        if self.page_title == 'Create New Item':
            messages.success(request, "Created new Item: %s" % self.item.title)
        else:
            messages.success(request, "Updated Item: %s" % self.item.title)

        return "%s?changed_id=%d" % (self.return_url, self.item.id)

    def redirect(self, request):
        return reverse('manage_item_image',
                       urlconf='inventory.urls',
                       args=[self.item.id])

    def setup_forms(self, form, request=None):
        i = 1
        if request:
            if self.item:
                form_set = [form(request.POST, instance=self.item)]
                if form_set[0].__class__.__name__ == "FurtherDetailForm" and (
                        settings.INVENTORY_MODE == "museum"):
                    for label in self.item.labels.all():
                        form = LabelForm(request.POST,
                                         instance=label,
                                         prefix=str(label.pk))
                        form.fields["text"].label = "Text %d" % i
                        form_set += [form]
                        i = i + 1
                    form_set += [LabelForm(request.POST)]
                    form_set[-1].fields["text"].label = "New Text"
                return form_set
            else:
                return [form(request.POST)]
        elif self.item:
            edit_form = form(instance=self.item)
            edit_form.fields['item_id'] = IntegerField(widget=HiddenInput(),
                                                       initial=self.item.id)
            form_set = [edit_form]
            if form_set[0].__class__.__name__ == "FurtherDetailForm" and (
                    settings.INVENTORY_MODE == "museum"):
                for label in self.item.labels.all():
                    form = LabelForm(instance=label,
                                     prefix=str(label.pk))
                    form.fields['text'].label = "Text %d" % i
                    form_set += [form]
                    i = i + 1
                form_set += [LabelForm(initial={'item': self.item})]
                form_set[-1].fields["text"].label = "New Text"
            return form_set
        else:
            return [form()]
