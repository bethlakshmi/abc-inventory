from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from inventory.models import Subitem
from inventory.views.default_view_text import make_subitem_messages
from inventory.views import InventoryFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class SubitemCreate(LoginRequiredMixin, InventoryFormMixin, CreateView):
    model = Subitem
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('subitems_list', urlconf="inventory.urls")
    page_title = 'Subitem'
    view_title = 'Create Subitem'
    valid_message = make_subitem_messages['create_success']
    intro_message = make_subitem_messages['create_intro']
    fields = ['title',
              'description',
              'subitem_number',
              'width',
              'height',
              'depth',
              'tags',
              'item']


class SubitemUpdate(LoginRequiredMixin, InventoryFormMixin, UpdateView):
    model = Subitem
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('subitems_list', urlconf="inventory.urls")
    page_title = 'Subitem'
    view_title = 'Update Subitem'
    valid_message = make_subitem_messages['edit_success']
    intro_message = make_subitem_messages['edit_intro']
    fields = ['title',
              'description',
              'subitem_number',
              'width',
              'height',
              'depth',
              'tags',
              'item']
