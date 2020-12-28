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
    StyleValue,
    StyleVersion,
)
from inventory.forms import ColorStyleValueForm
from django.contrib import messages


class ManageStyleVersion(View):
    object_type = StyleVersion
    template = 'inventory/manage_style_version.tmpl'
    page_title = 'Manage Style Settings'
    style_version = None

    def groundwork(self, request, args, kwargs):
        self.style_version = None
        version_id = kwargs.get("version_id")
        self.style_version = get_object_or_404(StyleVersion, id=version_id)

    def make_context(self, forms):
        title = "Creating New Style Version"
        if self.style_version:
            title = "Manage Styles Settings for %s, version %d" % (
                self.style_version.name,
                self.style_version.number)
        context = {
            'page_title': self.page_title,
            'title': title,
            'forms': forms,
        }
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManageStyleVersion, self).dispatch(*args, **kwargs)

    @never_cache
    def get(self, request, *args, **kwargs):
        redirect = self.groundwork(request, args, kwargs)
        forms = []
        for value in StyleValue.objects.filter(
                style_version=self.style_version).order_by(
                'style_property__selector__used_for',
                'style_property__selector__selector',
                'style_property__selector__pseudo_class'):
            form = ColorStyleValueForm(instance=value,
                                       prefix=str(value.pk),)
            form['value'].label = str(value.style_property.style_property)
            forms += [(value, form)]

        return render(request, self.template, self.make_context(forms))

    @never_cache
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if 'cancel' in list(request.POST.keys()):
            messages.success(request, "The last update was canceled.")
            return HttpResponseRedirect(reverse('items_list',
                                                urlconf='inventory.urls'))
        self.groundwork(request, args, kwargs)

        self.form = ItemImageForm(request.POST, request.FILES)
        if 'finish' in list(request.POST.keys()):
            if self.form.is_valid():
                self.item.images.all().delete()
                num_linked = 0
                num_uploaded = 0
                for image in self.form.cleaned_data['current_images']:
                    new_link = ItemImage(item=self.item, filer_image=image)
                    new_link.save()
                    num_linked = num_linked + 1
                files = request.FILES.getlist('new_images')
                if len(files) > 0:
                    filer_images = upload_and_attach(
                        files,
                        request.user,
                        self.item)
                    num_uploaded = len(filer_images)
                messages.success(
                    request,
                    ("Updated Item: %s<br>Linked %d images. Added %d " +
                     "images.") % (
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
