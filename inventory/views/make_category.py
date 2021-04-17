from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from inventory.models import Category
from inventory.views.default_view_text import make_category_messages
from inventory.views import InventoryFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class CategoryCreate(LoginRequiredMixin,
                     InventoryFormMixin,
                     CreateView):
    model = Category
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('categories_list', urlconf="inventory.urls")
    page_title = 'Category'
    view_title = 'Create Category'
    valid_message = make_category_messages['create_success']
    intro_message = make_category_messages['create_intro']
    fields = ['name', 'help_text']


class CategoryUpdate(LoginRequiredMixin,
                     InventoryFormMixin,
                     UpdateView):
    model = Category
    template_name = 'inventory/simple_form.tmpl'
    success_url = reverse_lazy('categories_list', urlconf="inventory.urls")
    page_title = 'Category'
    view_title = 'Update Category'
    valid_message = make_category_messages['edit_success']
    intro_message = make_category_messages['edit_intro']
    fields = ['name', 'help_text']
