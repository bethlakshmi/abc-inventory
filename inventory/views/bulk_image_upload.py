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


class BulkImageUpload(View):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Create New Item'
    first_title = 'Choose Pictures to Upload'
    second_title = 'Connect Pictures to Items'
    step = -1
    max = 1
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
            'next_form': None,
            'next_title': None},
    }

    def groundwork(self, request, args, kwargs):
        self.step = int(request.POST.get("step", -1))

    def make_post_forms(self, request):
        self.current_form_set = self.form_sets[self.step]
        if self.item:
            self.form = self.current_form_set['the_form'](
                request.POST,
                instance=self.item)
        else:
            self.form = self.current_form_set['the_form'](
                request.POST)

    def make_context(self, request):
        title = "Creating New Item"
        if self.item:
            title = self.item.title
        context = {
            'page_title': self.page_title,
            'title': title,
            'subtitle': self.current_form_set['next_title'],
            'forms': [self.form],
            'first': self.current_form_set['the_form'] is None,
            'last': self.form_sets[self.step+1]['next_form'] is None,
        }
        if str(self.form.__class__.__name__) == "PhysicalItemForm":
            context['special_handling'] = True
        return context

    def make_back_forms(self, request):
        self.step = self.step - 2
        self.current_form_set = self.form_sets[self.step]

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
        self.current_form_set = self.form_sets[-1]
        if self.item:
            self.form = self.current_form_set['next_form'](instance=self.item)
        else:
            self.form = self.current_form_set['next_form']()
        return render(request, self.template, self.make_context(request))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('items_list',
                                                urlconf='inventory.urls'))
        self.groundwork(request, args, kwargs)

        if 'next' in list(request.POST.keys()) or (
                'finish' in list(request.POST.keys())):
            self.make_post_forms(request)
            if not self.form.is_valid():
                self.step = self.step - 1
                self.current_form_set = self.form_sets[self.step]
                return render(request, self.template, self.make_context(
                    request))
            self.item = self.form.save()
            if 'finish' in list(request.POST.keys()):
                return self.finish(request)
        elif 'back' in list(request.POST.keys()):
            self.make_back_forms(request)
        else:
            messages.error(
                request,
                "Button Click Unclear.  If you did not tamper with the form," +
                " contact us.")
            self.current_form_set = {'next_form': None}

        if self.current_form_set['next_form'] is not None:
            self.form = self.current_form_set['next_form'](instance=self.item)
            self.form.fields['item_id'] = IntegerField(widget=HiddenInput(),
                                                       initial=self.item.id)
            return render(request, self.template, self.make_context(request))

        messages.error(request, "Unexpected logic flow.  Contact support.")

        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'), self.item.pk))
