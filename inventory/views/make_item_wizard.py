from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
    render,
)
from inventory.models import (
    Item,
)
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


class MakeItemWizard(View):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Create New Item'
    first_title = 'The Basics'
    second_title = 'Physical Information'
    third_title = 'Further Details'
    step = 0
    max = 3
    item = None

    def groundwork(self, request, args, kwargs):
        self.item = None
        if "item_id" in kwargs:
            self.page_title = 'Edit Item'
            item_id = kwargs.get("item_id")
            self.item = get_object_or_404(Item, id=item_id)
        elif request.POST and request.POST.get("item_id", False):
            self.item = get_object_or_404(Item,
                                          id=int(request.POST.get("item_id")))

    def make_post_forms(self, request):
        self.next_form = None
        step = request.POST.get("step", "0")
        if step == "0":
            the_form = BasicItemForm
            self.next_form = PhysicalItemForm
        elif step == "1":
            the_form = PhysicalItemForm
            self.next_form = FurtherDetailForm
        elif step == "2":
            the_form = FurtherDetailForm

        if self.item:
            self.form = the_form(
                request.POST,
                instance=self.item)
        else:
            self.form = the_form(
                request.POST)

    def make_context(self, request):
        context = {
            'page_title': self.page_title,
            'title': self.first_title,
            'forms': [self.form],
            'step': self.step,
            'max': self.max,
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MakeItemWizard, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        if redirect:
            return HttpResponseRedirect(redirect)
        if self.item:
            self.form = BasicItemForm(instance=self.item)
        else:
            self.form = BasicItemForm()
        return render(request, self.template, self.make_context(request))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        if redirect:
            return HttpResponseRedirect(redirect)

        self.make_post_forms(request)

        if not self.form.is_valid():
            return render(request, self.template, self.make_context(request))

        self.item = self.form.save()
        if self.next_form:
            self.form = self.next_form(instance=self.item)
            self.form.fields['item_id'] = IntegerField(widget=HiddenInput(),
                                                       initial=self.item.id)
            return render(request, self.template, self.make_context(request))

        if self.page_title == 'Create New Item':
            messages.success(request, "Created new Item: %s" % self.item.title)
        else:
            messages.success(request, "Updated Item: %s" % self.item.title)

        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'),
            self.item.id))
