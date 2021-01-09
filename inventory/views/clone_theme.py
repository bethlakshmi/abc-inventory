from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
    render,
)
from inventory.views import ManageTheme
from inventory.models import (
    StyleValue,
    StyleVersion,
    UserMessage,
)
from inventory.forms import (
    ColorStyleValueForm,
    ThemeVersionForm,
)
from django.contrib import messages
from inventory.views.default_view_text import user_messages
from datetime import datetime


class CloneTheme(ManageTheme):
    page_title = 'Clone Style Settings'
    title_format = "Clone Style Settings for %s, version %d"
    instruction_code = "CLONE_INSTRUCTIONS"

    def make_context(self, version_form, forms):
        context = super(CloneTheme, self).make_context(forms)
        context['version_form'] = version_form
        return context

    def setup_forms(self, request=None):
        forms = []
        for value in StyleValue.objects.filter(
                style_version=self.style_version).order_by(
                'style_property__selector__used_for',
                'style_property__selector__selector',
                'style_property__selector__pseudo_class',
                'style_property__style_property'):
            if request:
                version_form = ThemeVersionForm(request.POST)
                form = ColorStyleValueForm(request.POST,
                                           prefix=str(value.pk))
            else:
                version_form = ThemeVersionForm()
                form = ColorStyleValueForm(instance=value,
                                           prefix=str(value.pk))
            form['value'].label = str(value.style_property.style_property)
            forms += [(value, form)]
        return (version_form, forms)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CloneTheme, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        (version_form, forms) = self.setup_forms()
        return render(request,
                      self.template,
                      self.make_context(version_form, forms))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('themes_list',
                                                urlconf='inventory.urls'))
        self.groundwork(request, args, kwargs)
        (version_form, forms) = self.setup_forms(request)
        all_valid = True
        for value, form in forms:
            if not form.is_valid():
                all_valid = False
        if all_valid:
            for value, form in forms:
                form.save()
            self.style_version.updated_at = datetime.now()
            self.style_version.save()
            messages.success(request, "Updated %s" % self.style_version)
            if 'finish' in list(request.POST.keys()):
                return HttpResponseRedirect("%s?changed_id=%d" % (
                    reverse('themes_list', urlconf='inventory.urls'),
                    self.style_version.pk))
        else:
            messages.error(
                request,
                "Something was wrong, correct the errors below and try again.")

        return render(request, self.template, self.make_context(forms))