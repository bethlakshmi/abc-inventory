from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import (
    get_object_or_404,
    render,
)
from inventory.models import (
    Item,
)
from inventory.forms import ItemImageForm
from django.contrib import messages
from django.forms import (
    IntegerField,
    HiddenInput,
)


class ManageItemImage(View):
    object_type = Item
    template = 'inventory/item_wizard.tmpl'
    page_title = 'Manage Images'
    item = None

    def groundwork(self, request, args, kwargs):
        self.item = None
        item_id = kwargs.get("item_id")
        self.item = get_object_or_404(Item, id=item_id)

    def make_post_forms(self, request):
        self.current_form_set = self.form_sets[self.step]
        if self.item:
            self.form = self.current_form_set['the_form'](
                request.POST,
                instance=self.item)
        else:
            self.form = self.current_form_set['the_form'](
                request.POST)

    def make_context(self, request):
        title = "Creating New Item"
        if self.item:
            title = "Manage Images for %s" % self.item.title
        context = {
            'page_title': self.page_title,
            'title': title,
            'forms': [self.form],
        }
        return context

    def finish(self, request):
        if self.page_title == 'Create New Item':
            messages.success(request, "Created new Item: %s" % self.item.title)
        else:
            messages.success(request, "Updated Item: %s" % self.item.title)

        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'),
            self.item.id))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManageItemImage, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        self.form = ItemImageForm(initial={
            'current_images':  self.item.images.all()})
        return render(request, self.template, self.make_context(request))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass