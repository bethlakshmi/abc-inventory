from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render
from inventory.models import (
    Item,
)
from inventory.forms import BasicItemForm


class MakeItemWizard(View):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Create New Item'
    first_title = 'The Basics'
    second_title = 'Physical Information'
    third_title = 'Further Details'
    step = 0
    max = 3

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MakeItemWizard, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        form = BasicItemForm()
        context = {
            'page_title': self.page_title,
            'title': self.first_title,
            'forms': [form],
            'step': self.step,
            'max': self.max,
        }

        return render(request, self.template, context)
