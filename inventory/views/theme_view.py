from django.views.generic import View
from django.http import Http404
from django.http import (
    HttpResponse
)
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from inventory.models import StyleValue
from django.template import (
    Context,
    loader,
)


class ThemeView(View):
    template = 'inventory/style.css'

    def dispatch(self, *args, **kwargs):
        return super(ThemeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/css')
        context = {'selectors': {}}
        for value in StyleValue.objects.filter(
                style_version__currently_live=True):
            selector = value.style_property.selector
            if value.style_property.pseudo_class:
                selector = "%s:%s" % (selector,
                                      value.style_property.pseudo_class)
            if selector not in context['selectors'].keys():
                context['selectors'][selector] = {}
            context['selectors'][selector][
                value.style_property.style_property] = value.value
        t = loader.get_template(self.template)
        response.write(t.render(context))
        return response
