from inventory.views import GenericListView
from inventory.models import Act
from django.db.models import Count
from django.urls import reverse_lazy


class ActListView(GenericListView):
    object_type = Act
    template = 'inventory/act_list.tmpl'
    title = "Acts"

    def get_list(self):
        '''return self.object_type.objects.all().order_by('title').annotate(
            num_performers=Count('performers', distinct=True)).annotate(
            num_items=Count('item', distinct=True))'''
        return self.object_type.objects.all()
