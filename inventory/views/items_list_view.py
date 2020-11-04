from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from inventory.models import (
    Item,
)


class ItemsListView(View):
    object_type = Item
    template = 'inventory/item_list.tmpl'
    bid_order_fields = ('disposition', 'category')
    header = ("title", "description", "category", "disposition")
    title = "List of Items"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemsListView, self).dispatch(*args, **kwargs)

    def get_context_dict(self):
        return {'header': self.header,
                'title': self.title,
                'page_title': self.title,
                'items': self.get_list(),
                'changed_id': self.changed_id}

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.bid_order_fields)

    @never_cache
    def get(self, request, *args, **kwargs):
        if request.GET.get('changed_id'):
            self.changed_id = int(request.GET['changed_id'])
        else:
            self.changed_id = -1

        return render(request, self.template, self.get_context_dict())
