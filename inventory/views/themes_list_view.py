from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import StyleVersion


class ThemesListView(View):
    object_type = StyleVersion
    template = 'inventory/theme_list.tmpl'
    title = "List of Themes and Versions"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThemesListView, self).dispatch(*args, **kwargs)

    def get_context_dict(self, request):
        preview_version = None
        if hasattr(request.user, 'userstylepreview'):
            preview_version = request.user.userstylepreview.version

        return {
            'title': self.title,
            'page_title': self.title,
            'themes': self.object_type.objects.all(),
            'details_off': True,
            'changed_id': self.changed_id,
            'error_id': self.error_id,
            'preview': preview_version}

    @never_cache
    def get(self, request, *args, **kwargs):
        self.changed_id = int(request.GET.get('changed_id', default=-1))
        self.error_id = int(request.GET.get('error_id', default=-1))
        return render(request, self.template, self.get_context_dict(request))
