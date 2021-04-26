from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from inventory.models import Tag
from inventory.views.default_view_text import make_tag_messages
from inventory.views import (
    InventoryDeleteMixin,
    InventoryFormMixin,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class TagCreate(LoginRequiredMixin, InventoryFormMixin, CreateView):
    model = Tag
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('tags_list', urlconf="inventory.urls")
    page_title = 'Tag'
    view_title = 'Create Tag'
    valid_message = make_tag_messages['create_success']
    intro_message = make_tag_messages['create_intro']
    fields = ['name', 'help_text']


class TagUpdate(LoginRequiredMixin, InventoryFormMixin, UpdateView):
    model = Tag
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('tags_list', urlconf="inventory.urls")
    page_title = 'Tag'
    view_title = 'Update Tag'
    valid_message = make_tag_messages['edit_success']
    intro_message = make_tag_messages['edit_intro']
    fields = ['name', 'help_text']


class TagDelete(LoginRequiredMixin, InventoryDeleteMixin, DeleteView):
    model = Tag
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('tags_list', urlconf="inventory.urls")
    page_title = 'Tag'
    view_title = 'Delete Tag'
    valid_message = make_tag_messages['delete_success']
    intro_message = make_tag_messages['delete_intro']
