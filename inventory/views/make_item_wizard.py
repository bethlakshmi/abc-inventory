from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from inventory.models import (
    Item,
)
from inventory.forms import BasicItemForm
from django.contrib import messages


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

    def make_post_forms(self, request, the_form):
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
        self.form = BasicItemForm()
        return render(request, self.template, self.make_context(request))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # check bid validity
        self.make_post_forms(request, BasicItemForm)

        if not self.form.is_valid():
            context = self.make_context(request)
            return render(request, self.template, context)
        # save bid
        self.item = self.form.save()

        messages.success(request, "Created new Item: %s" % self.item.title)
        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'),
            self.item.pk))
