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
    ItemImage,
)
from filer.models import Image
from inventory.forms import ItemImageForm
from django.contrib import messages
from django.forms import (
    IntegerField,
    HiddenInput,
)
from inventory.functions import upload_and_attach


class ManageItemImage(View):
    object_type = Item
    template = 'inventory/manage_image.tmpl'
    page_title = 'Manage Images'
    item = None

    def groundwork(self, request, args, kwargs):
        self.item = None
        item_id = kwargs.get("item_id")
        self.item = get_object_or_404(Item, id=item_id)

    def make_context(self, request):
        title = "Creating New Item"
        if self.item:
            title = "Manage Images for %s" % self.item.title
        context = {
            'page_title': self.page_title,
            'title': title,
            'form': self.form,
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManageItemImage, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        self.form = ItemImageForm(initial={
            'current_images':  Image.objects.filter(itemimage__item=self.item)})
        return render(request, self.template, self.make_context(request))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('items_list',
                                                urlconf='inventory.urls'))
        self.groundwork(request, args, kwargs)

        if 'finish' in list(request.POST.keys()):
            self.form = ItemImageForm(request.POST, request.FILES)
            if self.form.is_valid():
                self.item.images.all().delete()
                num_linked = 0
                for image in self.form.cleaned_data['current_images']:
                    new_link = ItemImage(item=self.item, filer_image=image)
                    new_link.save()
                    num_linked = num_linked + 1
                files = request.FILES.getlist('new_images')
                if len(files) > 0:
                    num_uploaded = upload_and_attach(
                        files,
                        request.user,
                        self.item)
                messages.success(
                    request,
                    "Updated Item: %s<br>Linked %d images. Added %d images." % (
                        self.item.title,
                        num_linked,
                        num_uploaded))
                return HttpResponseRedirect("%s?changed_id=%d" % (
                    reverse('items_list', urlconf='inventory.urls'),
                    self.item.id))
        else:
            messages.error(
                request,
                "Button Click Unclear.  If you did not tamper with the form," +
                " contact us.")

        return render(request, self.template, self.make_context(request))