from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from inventory.models import Act
from inventory.views.default_view_text import make_act_messages
from inventory.views import (
    InventoryDeleteMixin,
    InventoryFormMixin,
)
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from inventory.forms import ActForm


class ActCreate(LoginRequiredMixin,
                CreatePopupMixin,
                InventoryFormMixin,
                CreateView):
    model = Act
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Act'
    view_title = 'Create Act'
    valid_message = make_act_messages['create_success']
    intro_message = make_act_messages['create_intro']
    form_class = ActForm


class ActUpdate(LoginRequiredMixin,
                UpdatePopupMixin,
                InventoryFormMixin,
                UpdateView):
    model = Act
    template_name = 'inventory/modal_make_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Act'
    view_title = 'Update Act'
    valid_message = make_act_messages['edit_success']
    intro_message = make_act_messages['edit_intro']
    form_class = ActForm


class ActDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Act
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Act'
    view_title = 'Delete Act'
    valid_message = make_act_messages['delete_success']
    intro_message = make_act_messages['delete_intro']
