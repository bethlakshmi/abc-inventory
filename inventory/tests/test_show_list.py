from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ActFactory,
    ItemFactory,
    ShowFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from inventory.models import Show


class TestShowList(TestCase):
    view_name = "shows_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.show = ShowFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_all_the_things(self):
        item = ItemFactory()
        other_item = ItemFactory()
        item.shows.set([self.show])
        other_item.shows.set([self.show])
        act = ActFactory()
        act.shows.set([self.show])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': '%d'" % self.show.pk)
        self.assertContains(response, "'title': '%s'" % self.show.title)
        self.assertContains(response, "'num_items': '2'")
        self.assertContains(response, "'num_acts': '1'")
        self.assertContains(
            response,
            "'description': '%s'" % self.show.description)
        self.assertContains(
            response,
            ('<a href="%s" title="Edit">%s&nbsp;&nbsp;<i class="fas ' +
             'fa-edit"></i></a>,<br><a href="%s" title=\"Edit\">%s&nbsp;' +
             '&nbsp;<i class="fas fa-edit"></i></a>') % (
             reverse("item_edit",
                     urlconf="inventory.urls",
                     args=[item.pk]),
             item.title,
             reverse("item_edit",
                     urlconf="inventory.urls",
                     args=[other_item.pk]),
             other_item.title))
        self.assertContains(
            response,
            ('<a href="%s" title="Edit">%s&nbsp;&nbsp;<i class="fas ' +
             'fa-edit"></i></a>,') % (
             reverse("act_update",
                     urlconf="inventory.urls",
                     args=[act.pk]),
             act.title))
        self.assertContains(
            response,
            reverse('show_create', urlconf="inventory.urls"))
        self.assertContains(
            response,
            reverse('show_update',
                    urlconf="inventory.urls",
                    args=[self.show.pk]))
        self.assertContains(
            response,
            reverse('show_delete',
                    urlconf="inventory.urls",
                    args=[self.show.pk]))

    def test_list_empty(self):
        from inventory.views.default_view_text import user_messages
        ex_url = "inventory/item/edit/"
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['ShowListView']['description'])
        self.assertContains(response, self.show.title)
        self.assertNotContains(response, ex_url)
        self.assertContains(response, "'num_items': '0'")

    def test_list_no_objects(self):
        from inventory.views.default_view_text import user_messages
        Show.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['ShowListView']['description'])
        self.assertNotContains(response, "'num_items': '")
