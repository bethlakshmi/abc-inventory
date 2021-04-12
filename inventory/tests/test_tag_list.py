from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ItemFactory,
    TagFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from inventory.models import Tag


class TestTagList(TestCase):
    view_name = "tags_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory()
        self.tag = TagFactory()
        self.item.tags.set([self.tag])
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_categories_basic(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['TagListView']['description'])
        self.assertContains(response, self.tag.name)
        self.assertContains(response, reverse(
            "item_edit",
            urlconf="inventory.urls",
            args=[self.item.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Tags</a>' % (
                self.url),
            html=True)

    def test_list_categories_all_the_things(self):
        another_tag = TagFactory()
        other_item = ItemFactory()
        other_item.tags.set([self.tag, another_tag])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': '%d'" % self.tag.pk)
        self.assertContains(response, "'id': '%d'" % another_tag.pk)
        self.assertContains(response, "'name': '%s'" % self.tag.name)
        self.assertContains(response, "'help': '%s'" % self.tag.help_text)
        self.assertContains(response, "'count': '2'")
        self.assertContains(response, "'count': '1'")
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
        self.assertContains(
            response,
            ('<a href="%s" title="Edit">%s&nbsp;&nbsp;<i class="fas ' +
             'fa-edit"></i></a>') % (
             reverse("item_edit",
                     urlconf="inventory.urls",
                     args=[other_item.pk]),
             other_item.title),
            2)

    def test_list_tag_empty(self):
        from inventory.views.default_view_text import user_messages
        ex_url = reverse("item_edit",
                         urlconf="inventory.urls",
                         args=[self.item.pk])
        self.item.delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['TagListView']['description'])
        self.assertContains(response, self.tag.name)
        self.assertNotContains(response, ex_url)
        self.assertContains(response, "'count': '0'")

    def test_list_no_tags(self):
        from inventory.views.default_view_text import user_messages
        Tag.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['TagListView']['description'])
        self.assertNotContains(response, "'count': '")
        self.assertNotContains(response, self.item.title)
