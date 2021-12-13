from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from inventory.models import Subitem
from inventory.forms import (
    SubitemForm,
    TroupeSubitemForm,
)
from inventory.views.default_view_text import make_subitem_messages
from inventory.views import (
    InventoryDeleteMixin,
    InventoryFormMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from settings import INVENTORY_MODE


class SubitemCreate(LoginRequiredMixin, InventoryFormMixin, CreateView):
    model = Subitem
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('subitems_list', urlconf="inventory.urls")
    page_title = 'Subitem'
    view_title = 'Create Subitem'
    valid_message = make_subitem_messages['create_success']
    intro_message = make_subitem_messages['create_intro']
    form_class = SubitemForm

    def get_form_class(self):
        form = super().get_form_class()
        if INVENTORY_MODE == "troupe":
            form = TroupeSubitemForm
        return form


class SubitemUpdate(LoginRequiredMixin, InventoryFormMixin, UpdateView):
    model = Subitem
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('subitems_list', urlconf="inventory.urls")
    page_title = 'Subitem'
    view_title = 'Update Subitem'
    valid_message = make_subitem_messages['edit_success']
    intro_message = make_subitem_messages['edit_intro']
    form_class = SubitemForm

    def get_form_class(self):
        form = super().get_form_class()
        if INVENTORY_MODE == "troupe":
            form = TroupeSubitemForm
        return form


class SubitemDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Subitem
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('subitems_list', urlconf="inventory.urls")
    page_title = 'Subitem'
    view_title = 'Delete Subitem'
    valid_message = make_subitem_messages['delete_success']
    intro_message = make_subitem_messages['delete_intro']
