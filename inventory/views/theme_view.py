from django.views.generic import View
from django.http import Http404
from django.http import (
    HttpResponse
)
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from inventory.models import UserMessage
from inventory.views.default_view_text import user_messages
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
        context = {
            'inventory_primary_color': '#fff',
            'inventory_primary_background_color': '#ffc0cb',
            'inventory_primary_border_color': '#ffc0cb',
            'inventory_primary_color_hover': '#fff',
            'inventory_primary_background_color_hover': '#fe019a',
            'inventory_primary_border_color_hover': '#fe019a',
        }
        t = loader.get_template(self.template)
        response.write(t.render(context))
        return response
