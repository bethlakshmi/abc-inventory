from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from inventory.models import Show
from inventory.views.default_view_text import make_show_messages
from inventory.views import (
    InventoryDeleteMixin,
    InventoryFormMixin,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ShowCreate(LoginRequiredMixin,
                 CreatePopupMixin,
                 InventoryFormMixin,
                 CreateView):
    model = Show
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Show'
    view_title = 'Create Show'
    valid_message = make_show_messages['create_success']
    intro_message = make_show_messages['create_intro']
    fields = ['title',
              'description',
              'first_performed',
              'last_performed',
              'venue_name',
              'city']


class ShowUpdate(LoginRequiredMixin,
                 UpdatePopupMixin,
                 InventoryFormMixin,
                 UpdateView):
    model = Show
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Show'
    view_title = 'Update Show'
    valid_message = make_show_messages['edit_success']
    intro_message = make_show_messages['edit_intro']
    fields = ['title',
              'description',
              'first_performed',
              'last_performed',
              'venue_name',
              'city']


class ShowDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Show
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Show'
    view_title = 'Delete Show'
    valid_message = make_show_messages['delete_success']
    intro_message = make_show_messages['delete_intro']
