from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import (
    Item,
    UserMessage,
)
from django.urls import reverse
from inventory.views.default_view_text import user_messages
from django.conf import settings


class GenericListView(View):
    ##############
    #  This is an abstract class, it gives the logic for rendering a list
    #  using something that extends the item_list.tmpl:
    #     - order_fields or get_list - either tell the system what order to
    #       use when getting items, or redefine get_list yourself.
    #     - title - heading for the top of the page
    # Optional stuff:
    #     - form_url = for a form that is a set of checkboxes and a button
    #          called "Merge" - the checkboxes will be named for the plural
    #          of the object_type, and have values of the "id" column in the
    #          table
    #     - the GET request can use changed_id or error_id to provide success
    #          or error color coding for any changes to the list of objects
    ##############
    object_type = Item
    template = 'inventory/item_list.tmpl'
    title = "Generic List"
    form_url = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GenericListView, self).dispatch(*args, **kwargs)

    def get_context_dict(self, museum_on):
        verbose = self.object_type._meta.verbose_name_plural
        context = {
            'museum_on': museum_on,
            'title': self.title,
            'page_title': self.title,
            'items': self.get_list(),
            'changed_id': self.changed_id,
            'error_id': self.error_id,
            'data_name_plural': verbose.title().lower(),
            'path_list': [
                ("Item List", reverse('items_list', urlconf='inventory.urls')),
                ("SubItem List",
                 reverse('subitems_list', urlconf='inventory.urls')),
                ("Categories",
                 reverse('categories_list', urlconf='inventory.urls')),
                ("Tags", reverse('tags_list', urlconf='inventory.urls')),
                ]}
        if not museum_on:
            context["path_list"] += [
                ("Shows", reverse('shows_list', urlconf='inventory.urls')),
                ("Acts", reverse('acts_list', urlconf='inventory.urls')),
                ("Performers",
                 reverse('performers_list', urlconf='inventory.urls')),
                ]
        if self.__class__.__name__ in user_messages:
            context['instructions'] = UserMessage.objects.get_or_create(
                view=self.__class__.__name__,
                code="%s_INSTRUCTIONS" % self.__class__.__name__.upper(),
                defaults={
                    'summary': user_messages[self.__class__.__name__][
                        'summary'],
                    'description': user_messages[self.__class__.__name__][
                        'description']}
                )[0].description
        if self.form_url:
            context['form_url'] = self.form_url
            verbose = self.object_type._meta.verbose_name_plural
            context['data_name_plural'] = verbose.title().lower()
        return context

    def get_list(self):
        return self.object_type.objects.filter().order_by(
            *self.order_fields)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.museum_on = True
        if settings.INVENTORY_MODE == "troupe":
            self.museum_on = False
        self.changed_id = int(request.GET.get('changed_id', default=-1))
        self.error_id = int(request.GET.get('error_id', default=-1))
        return render(request, self.template, self.get_context_dict(
            self.museum_on))
