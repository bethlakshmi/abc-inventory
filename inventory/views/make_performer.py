from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from inventory.models import Performer
from inventory.views.default_view_text import make_performer_messages
from inventory.views import (
    InventoryDeleteMixin,
    InventoryFormMixin,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class PerformerCreate(LoginRequiredMixin,
                      CreatePopupMixin,
                      InventoryFormMixin,
                      CreateView):
    model = Performer
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Performer'
    view_title = 'Create Performer'
    valid_message = make_performer_messages['create_success']
    intro_message = make_performer_messages['create_intro']
    fields = ['name', 'size_info', 'description']


class PerformerUpdate(LoginRequiredMixin,
                      UpdatePopupMixin,
                      InventoryFormMixin,
                      UpdateView):
    model = Performer
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Performer'
    view_title = 'Update Performer'
    valid_message = make_performer_messages['edit_success']
    intro_message = make_performer_messages['edit_intro']
    fields = ['name', 'size_info', 'description']


class PerformerDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Performer
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Performer'
    view_title = 'Delete Performer'
    valid_message = make_performer_messages['delete_success']
    intro_message = make_performer_messages['delete_intro']
