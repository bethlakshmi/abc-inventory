from inventory.views import ItemsListView
from inventory.models import Category
from django.db.models import Count


class CategoryListView(ItemsListView):
    object_type = Category
    template = 'inventory/category_list.tmpl'
    order_fields = ('name', )
    title = "Categories"

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(num_items=Count('items'))
