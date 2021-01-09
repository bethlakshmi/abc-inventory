from inventory.views import ItemsListView
from inventory.models import Subitem


class SubItemsListView(ItemsListView):
    object_type = Subitem
    template = 'inventory/subitem_list.tmpl'
    order_fields = ('item__disposition', 'item__category')
    title = "List of Items"
