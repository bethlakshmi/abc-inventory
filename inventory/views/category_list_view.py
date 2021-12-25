from inventory.views import GenericListView
from inventory.models import Category
from django.db.models import Count
from django.urls import reverse_lazy


class CategoryListView(GenericListView):
    object_type = Category
    template = 'inventory/category_list.tmpl'
    order_fields = ('name', )
    title = "Categories"
    form_url = reverse_lazy('category_merge', urlconf='inventory.urls')

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields).annotate(num_items=Count('items'))
