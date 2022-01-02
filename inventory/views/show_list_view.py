from inventory.views import GenericListView
from inventory.models import Show
from django.db.models import Count
from django.urls import reverse_lazy


class ShowListView(GenericListView):
    object_type = Show
    template = 'inventory/show_list.tmpl'
    order_fields = ('title', )
    title = "Shows"

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(
            num_items=Count('item'),
            num_acts=Count('act'))
