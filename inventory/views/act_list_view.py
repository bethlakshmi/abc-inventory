from inventory.views import GenericListView
from inventory.models import Act
from django.db.models import Count
from django.urls import reverse_lazy


class ActListView(GenericListView):
    object_type = Act
    template = 'inventory/act_list.tmpl'
    order_fields = ('title', )
    title = "Acts"

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(
            num_items=Count('item'),
            num_performers=Count('performers'))
