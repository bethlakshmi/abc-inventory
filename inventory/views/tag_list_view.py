from inventory.views import ItemsListView
from inventory.models import Tag
from django.db.models import Count


class TagListView(ItemsListView):
    object_type = Tag
    template = 'inventory/tag_list.tmpl'
    order_fields = ('name', )
    title = "Tags"

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(num_items=Count('items'))
