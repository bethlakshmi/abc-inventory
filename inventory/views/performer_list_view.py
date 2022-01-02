from inventory.views import GenericListView
from inventory.models import Performer
from django.db.models import Count
from django.urls import reverse_lazy


class PerformerListView(GenericListView):
    object_type = Performer
    template = 'inventory/performer_list.tmpl'
    order_fields = ('name', )
    title = "Performers"

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(
            num_items=Count('items'),
            num_acts=Count('acts'),
            num_shows=Count('shows'))
