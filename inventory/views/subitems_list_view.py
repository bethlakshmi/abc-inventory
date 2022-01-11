from inventory.views import GenericListView
from inventory.models import Subitem


class SubItemsListView(GenericListView):
    object_type = Subitem
    template = 'inventory/subitem_list.tmpl'
    order_fields = ('item__disposition', 'item__category')
    title = "List of SubItems"
