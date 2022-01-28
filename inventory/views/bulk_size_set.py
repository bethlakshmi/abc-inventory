from extra_views import FormSetSuccessMessageMixin, ModelFormSetView
from django.urls import reverse_lazy
from inventory.models import (
    Item,
    UserMessage,
)
from inventory.views.default_view_text import edit_size_messages
from inventory.forms import SizeSetForm
from django.contrib.auth.mixins import LoginRequiredMixin


class BulkSizeSet(LoginRequiredMixin,
                  FormSetSuccessMessageMixin,
                  ModelFormSetView):
    model = Item
    form_class = SizeSetForm
    factory_kwargs = {'extra': 0}
    template_name = 'inventory/bulk_size_formset.tmpl'
    intro_message = edit_size_messages['intro']
    page_title = "Bulk Size Settings"
    view_title = "Bulk Size Settings"
    success_url = reverse_lazy('item_list', urlconf="inventory.urls")

    def get_context_data(self, **kwargs):
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="INTRO",
            defaults={
                'summary': "Successful Submission",
                'description': self.intro_message})
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['special_handling'] = True
        context['title'] = self.view_title
        context['instructions'] = msg[0].description
        context['return_url'] = self.request.GET.get('next', self.success_url)
        return context

    def get_queryset(self):
        query = super(BulkSizeSet, self).get_queryset()
        query = query.filter(sz__in=['', '[]']).exclude(size__exact='')
        return query

    def get_success_message(self, formset):
        names = []
        name_list = ""
        for form in formset.forms:
            names += [form.instance.title]
        for name in names:
            if len(name_list) == 0:
                name_list = name
            else:
                name_list = "%s, %s" % (name, name_list)
        return '{} item sizes were updated.'.format(name_list)

    def get_success_url(self):
        return "%s?changed_ids=[%s]&obj_type=%s" % (
            self.request.GET.get('next', self.success_url),
            self.changed_id,
            self.obj_type)
