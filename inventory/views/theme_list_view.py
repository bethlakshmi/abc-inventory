from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import StyleVersion


class ThemeListView(View):
    object_type = Item
    template = 'inventory/version_list.tmpl'
    title = "List of Themes and Versions"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThemeListView, self).dispatch(*args, **kwargs)

    def get_context_dict(self):
        return {
            'title': self.title,
            'page_title': self.title,
            'items': self.object_type.objects.filter(),
            'changed_id': self.changed_id}

    @never_cache
    def get(self, request, *args, **kwargs):
        self.changed_id = int(request.GET.get('changed_id', default=-1))
        return render(request, self.template, self.get_context_dict())
