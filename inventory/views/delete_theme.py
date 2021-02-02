from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from inventory.models import StyleVersion
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages


class DeleteTheme(View):
    object_type = StyleVersion

    def groundwork(self, request, args, kwargs):
        self.style_version = None
        version_id = kwargs.get("version_id")
        self.style_version = get_object_or_404(StyleVersion, id=version_id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteTheme, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        self.style_version.delete()
        messages.success(request, "Deleted Theme %s" % str(self.style_version))
        return HttpResponseRedirect(reverse('themes_list',
                                            urlconf='inventory.urls'))
