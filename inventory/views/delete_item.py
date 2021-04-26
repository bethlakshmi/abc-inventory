from django.views.generic.edit import DeleteView
from inventory.models import Item
from inventory.views.default_view_text import delete_item_messages
from inventory.views import InventoryDeleteMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ItemDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Item
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('items_list', urlconf="inventory.urls")
    page_title = 'Item'
    view_title = 'Delete Item'
    valid_message = delete_item_messages['delete_success']
    intro_message = delete_item_messages['delete_intro']
