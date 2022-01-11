from inventory.views import GenericListView
from inventory.models import Performer
from django.db.models import Count
from django.urls import reverse_lazy


class PerformerListView(GenericListView):
    object_type = Performer
    template = 'inventory/performer_list.tmpl'
    title = "Performers"

    def get_list(self):
        return self.object_type.objects.filter().order_by('name').annotate(
            num_items=Count('item', distinct=True)).annotate(
            num_acts=Count('act', distinct=True))
