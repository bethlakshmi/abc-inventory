from inventory.views import GenericListView
from inventory.models import Tag
from django.db.models import Count
from django.urls import reverse_lazy


class TagListView(GenericListView):
    object_type = Tag
    template = 'inventory/tag_list.tmpl'
    order_fields = ('name', )
    title = "Tags"
    form_url = reverse_lazy('tag_merge', urlconf='inventory.urls')

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(num_items=Count('items'))
