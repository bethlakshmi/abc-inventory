from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from inventory.models import ItemImage
from django.contrib import messages


class PromoteItemImage(View):
    object_type = ItemImage
    itemimage = None

    def groundwork(self, request, args, kwargs):
        self.itemimage = None
        itemimage_id = kwargs.get("itemimage_id")
        self.itemimage = get_object_or_404(ItemImage, id=itemimage_id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PromoteItemImage, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        self.groundwork(request, args, kwargs)
        self.itemimage.main_image = True
        self.itemimage.save()
        messages.success(request, "Set Main Image for %s to image file %s" % (
            self.itemimage.item,
            self.itemimage.filer_image))
        return HttpResponseRedirect("%s?changed_id=%d" % (
            reverse('items_list', urlconf='inventory.urls'),
            self.itemimage.item.pk))
