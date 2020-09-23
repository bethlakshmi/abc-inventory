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
    step = -1
    max = 1
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
        self.step = int(request.POST.get("step", -1))

    def make_post_forms(self, request):
        self.next_form = None
        self.title = None
        self.next_title = None
        if self.step == 0:
            the_form = BasicItemForm
            self.next_form = PhysicalItemForm
            self.title = self.first_title
            self.next_title = self.second_title
        elif self.step == 1:
            the_form = PhysicalItemForm
            self.next_form = FurtherDetailForm
            self.title = self.second_title
            self.next_title = self.third_title
        elif self.step == 2:
            the_form = FurtherDetailForm
            self.title = self.third_title

        if self.item:
            self.form = the_form(
                request.POST,
                instance=self.item)
        else:
            self.form = the_form(
                request.POST)

    def make_context(self, request, title):
        context = {
            'page_title': self.page_title,
            'title': title,
            'forms': [self.form],
            'step': self.step,
            'max': self.max,
        }
        return context

    def make_back_forms(self, request):
        self.next_form = None
        self.title = None
        self.next_title = None
        if self.step == 1:
            self.next_form = BasicItemForm
            self.next_title = self.first_title
        elif self.step == 2:
            self.next_form = PhysicalItemForm
            self.next_title = self.second_title
        self.step = self.step - 2

    def finish(self, request):
        if self.page_title == 'Create New Item':
            messages.success(request, "Created new Item: %s" % self.item.title)
        else:
            messages.success(request, "Updated Item: %s" % self.item.title)

        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'),
            self.item.id))

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
        return render(request, self.template, self.make_context(
            request,
            self.first_title))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('items_list',
                                                urlconf='inventory.urls'))
        redirect = self.groundwork(request, args, kwargs)
        if redirect:
            return HttpResponseRedirect(redirect)
        if 'next' in list(request.POST.keys()) or (
                'finish' in list(request.POST.keys())):
            self.make_post_forms(request)
            if not self.form.is_valid():
                return render(request, self.template, self.make_context(
                    request,
                    self.title))
            self.item = self.form.save()
            if 'finish' in list(request.POST.keys()):
                return self.finish(request)
        elif 'back' in list(request.POST.keys()):
            self.make_back_forms(request)
        else:
            raise Exception("button click unclear")

        if self.next_form:
            self.form = self.next_form(instance=self.item)
            self.form.fields['item_id'] = IntegerField(widget=HiddenInput(),
                                                       initial=self.item.id)
            return render(request, self.template, self.make_context(
                request,
                self.next_title))

        messages.error(request, "Unexpected logic flow.  Call Betty")

        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'), self.item.id))
