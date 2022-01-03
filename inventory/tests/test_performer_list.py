from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ActFactory,
    ItemFactory,
    PerformerFactory,
    ShowFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from inventory.models import Performer


class TestPerformerList(TestCase):
    view_name = "performers_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.performer = PerformerFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_all_the_things(self):
        item = ItemFactory()
        other_item = ItemFactory()
        item.performers.set([self.performer])
        other_item.performers.set([self.performer])
        act = ActFactory()
        act.performers.set([self.performer])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': '%d'" % self.performer.pk)
        self.assertContains(response, "'name': '%s'" % self.performer.name)
        self.assertContains(response, "'num_items': '2'")
        self.assertContains(response, "'num_acts': '1'")
        self.assertContains(
            response,
            "'description': '%s'" % self.performer.description)
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
             reverse("performer_update",
                     urlconf="inventory.urls",
                     args=[performer.pk]),
             performer.name))
        self.assertContains(
            response,
            ('<a href="%s" title="Edit">%s&nbsp;&nbsp;<i class="fas ' +
             'fa-edit"></i></a>,') % (
             reverse("show_update",
                     urlconf="inventory.urls",
                     args=[show.pk]),
             show.title))
        self.assertContains(
            response,
            reverse('act_create', urlconf="inventory.urls"))
        self.assertContains(
            response,
            reverse('act_update',
                    urlconf="inventory.urls",
                    args=[self.act.pk]))
        self.assertContains(
            response,
            reverse('act_delete',
                    urlconf="inventory.urls",
                    args=[self.act.pk]))

    def test_list_act_empty(self):
        from inventory.views.default_view_text import user_messages
        ex_url = "inventory/item/edit/"
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['ActListView']['description'])
        self.assertContains(response, self.act.title)
        self.assertNotContains(response, ex_url)
        self.assertContains(response, "'num_items': '0'")

    def test_list_no_acts(self):
        from inventory.views.default_view_text import user_messages
        Act.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response,
                            user_messages['ActListView']['description'])
        self.assertNotContains(response, "'num_items': '")
