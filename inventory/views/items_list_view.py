from inventory.models import Item
from inventory.views import GenericListView


class ItemsListView(GenericListView):
    object_type = Item
    template = 'inventory/item_list.tmpl'
    order_fields = ('disposition', 'category')
    title = "List of Items"
    form_url = None

    def get_list(self):
        item_list = super(ItemsListView, self).get_list()
        if self.museum_on:
            item_list = item_list.select_related(
                'category',
                'disposition').prefetch_related(
                'images',
                'subitem_set',
                'tags',
                'connections')
        else:
            item_list = item_list.select_related(
                'category',
                'disposition').prefetch_related(
                'images',
                'subitem_set',
                'tags', 'acts',
                'performers',
                'shows',
                'colors')
        return item_list
