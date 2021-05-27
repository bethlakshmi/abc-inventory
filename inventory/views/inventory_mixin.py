from django.views.generic.edit import (
    DeletionMixin,
    ModelFormMixin,
    SingleObjectMixin,
)
from django.contrib import messages
from inventory.models import UserMessage


class InventoryFormMixin(ModelFormMixin):
    def get_context_data(self, **kwargs):
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="INTRO",
            defaults={
                'summary': "Successful Submission",
                'description': self.intro_message})
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['view_title'] = self.view_title
        context['instructions'] = msg[0].description
        context['form'].required_css_class = 'required'
        context['cancel_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="SUCCESS",
            defaults={
                'summary': "Successful Submission",
                'description': self.valid_message})
        messages.success(self.request, msg[0].description % str(self.object))
        return response

    def get_success_url(self):
        return "%s?changed_id=%s" % (self.success_url, self.object.pk)


class InventoryDeleteMixin(DeletionMixin, SingleObjectMixin):
    def get_context_data(self, **kwargs):
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="INTRO",
            defaults={
                'summary': "Successful Submission",
                'description': self.intro_message})
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['view_title'] = self.view_title
        context['instructions'] = msg[0].description % self.object
        context['cancel_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = UserMessage.objects.get_or_create(
            view=self.__class__.__name__,
            code="SUCCESS",
            defaults={
                'summary': "Successful Submission",
                'description': self.valid_message})
        messages.success(request, msg[0].description % str(self.object))
        return response
