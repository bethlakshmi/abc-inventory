from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from inventory.models import StyleVersion
from django.contrib import messages


class ActivateTheme(View):
    object_type = StyleVersion
    style_version = None

    def groundwork(self, request, args, kwargs):
        self.style_version = None
        version_id = kwargs.get("version_id")
        self.style_version = get_object_or_404(StyleVersion, id=version_id)
        self.target = kwargs.get("target_system")
        if self.target not in ("test", "live"):
            raise Http404

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ActivateTheme, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        current = None
        if self.target == "live":
            current = StyleVersion.objects.get(currently_live=True)
            current.currently_live = False
            self.style_version.currently_live = True
        else:
            current = StyleVersion.objects.get(currently_live=True)
            current.currently_test = False
            self.style_version.currently_test = True
        current.save()
        self.style_version.save()
        messages.success(request, "Activated %s on %s" % (
            self.style_version,
            self.target))
        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('themes_list', urlconf='inventory.urls'),
            self.style_version.pk))
