from django.shortcuts import get_object_or_404
from inventory.views import GenericWizard
from inventory.models import Item
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


class MakeItemWizard(GenericWizard):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Create New Item'
    first_title = 'The Basics'
    second_title = 'Physical Information'
    third_title = 'Further Details'
    item = None
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
        if str(self.forms[0].__class__.__name__) == "PhysicalItemForm":
            context['special_handling'] = True
        return context

    def finish_valid_form(self, request):
        self.item = self.forms[0].save()

    def finish(self, request):
        if self.page_title == 'Create New Item':
            messages.success(request, "Created new Item: %s" % self.item.title)
        else:
            messages.success(request, "Updated Item: %s" % self.item.title)

        return "%s?changed_id=%d" % (self.return_url, self.item.id)

    def setup_forms(self, form, POST=None):
        if POST:
            if self.item:
                return [form(POST, instance=self.item)]
            else:
                return [form(POST)]
        elif self.item:
            edit_form = form(instance=self.item)
            edit_form.fields['item_id'] = IntegerField(widget=HiddenInput(),
                                                       initial=self.item.id)
            return [edit_form]
        else:
            return [form()]
