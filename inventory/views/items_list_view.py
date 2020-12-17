from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import Item
from django.urls import reverse


class ItemsListView(View):
    object_type = Item
    template = 'inventory/item_list.tmpl'
    bid_order_fields = ('disposition', 'category')
    title = "List of Items"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemsListView, self).dispatch(*args, **kwargs)

    def get_context_dict(self):
        return {
        'title': self.title,
        'page_title': self.title,
        'items': self.get_list(),
        'changed_id': self.changed_id,
        'path_list': [
            ("Item List", reverse('items_list', urlconf='inventory.urls')),
            ("SubItem List",
             reverse('subitems_list', urlconf='inventory.urls'))]}

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.bid_order_fields)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.changed_id = int(request.GET.get('changed_id', default=-1))
        return render(request, self.template, self.get_context_dict())
