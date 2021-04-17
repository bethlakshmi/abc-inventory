from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    CategoryFactory,
    ItemFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from inventory.models import Category


class TestCategoryList(TestCase):
    view_name = "categories_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory(category=CategoryFactory())
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_categories_basic(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['CategoryListView']['description'])
        self.assertContains(response, self.item.category.name)
        self.assertContains(response, reverse(
            "item_edit",
            urlconf="inventory.urls",
            args=[self.item.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Categories</a>' % (
                self.url),
            html=True)

    def test_list_categories_all_the_things(self):
        other_item = ItemFactory(category=self.item.category)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': '%d'" % self.item.category.pk)
        self.assertContains(response, "'name': '%s'" % self.item.category.name)
        self.assertContains(response,
                            "'help': '%s'" % self.item.category.help_text)
        self.assertContains(response, "'count': '2'")
        self.assertContains(
            response,
            ('<a href="%s" title="Edit">%s&nbsp;&nbsp;<i class="fas ' +
             'fa-edit"></i></a>,<br><a href="%s" title=\"Edit\">%s&nbsp;' +
             '&nbsp;<i class="fas fa-edit"></i></a>') % (
             reverse("item_edit",
                     urlconf="inventory.urls",
                     args=[self.item.pk]),
             self.item.title,
             reverse("item_edit",
                     urlconf="inventory.urls",
                     args=[other_item.pk]),
             other_item.title))

    def test_list_category_empty(self):
        from inventory.views.default_view_text import user_messages
        category = self.item.category
        ex_url = reverse("item_edit",
                         urlconf="inventory.urls",
                         args=[self.item.pk])
        self.item.delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['CategoryListView']['description'])
        self.assertContains(response, category.name)
        self.assertNotContains(response, ex_url)
        self.assertContains(response, "'count': '0'")

    def test_list_no_categories(self):
        from inventory.views.default_view_text import user_messages
        Category.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['CategoryListView']['description'])
        self.assertNotContains(response, "'count': '")
