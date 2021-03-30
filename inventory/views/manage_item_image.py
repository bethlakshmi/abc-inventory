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
from inventory.models import (
    Item,
    ItemImage,
    UserMessage,
)
from filer.models import Image
from inventory.forms import ItemImageForm
from django.contrib import messages
from inventory.functions import upload_and_attach
from inventory.views.default_view_text import user_messages


class ManageItemImage(View):
    object_type = Item
    template = 'inventory/manage_image.tmpl'
    page_title = 'Manage Images'
    item = None
    instruction_code = "MANAGE_ITEM_IMAGE_INSTRUCT"

    def groundwork(self, request, args, kwargs):
        self.item = None
        item_id = kwargs.get("item_id")
        self.item = get_object_or_404(Item, id=item_id)

    def make_context(self, request):
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code=self.instruction_code,
            defaults={
                'summary': user_messages[self.instruction_code]['summary'],
                'description': user_messages[self.instruction_code][
                    'description']})
        title = "Manage Images for %s" % self.item.title
        context = {
            'page_title': self.page_title,
            'title': title,
            'form': self.form,
            'instructions': msg[0].description,
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManageItemImage, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        item_images = Image.objects.filter(itemimage__item=self.item)
        self.form = ItemImageForm(initial={'current_images':  item_images})
        self.form.fields['current_images'].queryset = item_images
        self.form.fields['other_images'].queryset = self.form.fields[
            'other_images'].queryset.exclude(itemimage__item=self.item)
        return render(request, self.template, self.make_context(request))

    def link_images(self, images):
        num_linked = 0
        for image in images:
            new_link = ItemImage(item=self.item, filer_image=image)
            new_link.save()
            num_linked = num_linked + 1
        return num_linked

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('items_list',
                                                urlconf='inventory.urls'))
        self.groundwork(request, args, kwargs)
        item_images = Image.objects.filter(itemimage__item=self.item)
        self.form = ItemImageForm(request.POST, request.FILES)
        self.form.fields['current_images'].queryset = item_images
        self.form.fields['other_images'].queryset = self.form.fields[
            'other_images'].queryset.exclude(itemimage__item=self.item)

        if 'finish' in list(request.POST.keys()):
            if self.form.is_valid():
                num_linked = 0
                num_uploaded = 0
                num_removed = 0
                current_image_files = []
                for existing in self.item.images.all():
                    if existing.filer_image not in self.form.cleaned_data[
                            'current_images']:
                        existing.delete()
                        self.item.save()
                        num_removed = num_removed + 1
                    else:
                        current_image_files += [existing.filer_image]

                num_linked = num_linked + self.link_images(
                    self.form.cleaned_data['unattached_images'])
                num_linked = num_linked + self.link_images(
                    self.form.cleaned_data['other_images'])

                files = request.FILES.getlist('new_images')
                if len(files) > 0:
                    filer_images = upload_and_attach(
                        files,
                        request.user,
                        self.item)
                    num_uploaded = len(filer_images)

                for image in self.form.cleaned_data['delete_images']:
                    image.delete()
                if len(self.form.cleaned_data['delete_images']) > 0:
                    messages.success(
                        request,
                        "Deleted %d images." % (
                            len(self.form.cleaned_data['delete_images'])))
                messages.success(
                    request,
                    ("Updated Item: %s<br>Linked %d images. Added %d " +
                     "images.  Unlinked %d images.") % (
                        self.item.title,
                        num_linked,
                        num_uploaded,
                        num_removed))
                return HttpResponseRedirect("%s?changed_id=%d" % (
                    reverse('items_list', urlconf='inventory.urls'),
                    self.item.id))
        else:
            messages.error(
                request,
                "Button Click Unclear.  If you did not tamper with the form," +
                " contact us.")

        return render(request, self.template, self.make_context(request))
