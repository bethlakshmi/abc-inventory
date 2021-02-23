from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from inventory.models import (
    StyleVersion,
    UserStylePreview,
)
from django.contrib import messages


class PreviewTheme(View):
    style_version = None

    def groundwork(self, request, args, kwargs):
        self.style_version = None
        version_id = int(kwargs.get("version_id", -1))
        if version_id >= 0:
            self.style_version = get_object_or_404(StyleVersion, id=version_id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PreviewTheme, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        changed_id = None
        if self.style_version is None:
            if hasattr(request.user, 'userstylepreview'):
                changed_id = request.user.userstylepreview.version.pk
                msg = "Deactivating preview of version: " + str(
                    request.user.userstylepreview.version)
                request.user.userstylepreview.delete()
            else:
                msg = "No style was currently previewed."
        else:
            preview = None
            if hasattr(request.user, 'userstylepreview'):
                preview = request.user.userstylepreview
                preview.version = self.style_version
            else:
                preview = UserStylePreview(version=self.style_version,
                                           previewer=request.user)
            msg = "Setting preview version to: " + str(preview.version)
            preview.save()
            changed_id = preview.version.pk
        messages.success(request, msg)
        theme_list = reverse('themes_list', urlconf='inventory.urls')
        if changed_id is not None:
            theme_list = "%s?changed_id=%d" % (theme_list, changed_id)
        return HttpResponseRedirect(theme_list)
