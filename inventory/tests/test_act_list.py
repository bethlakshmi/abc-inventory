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
from inventory.models import Act


class TestActList(TestCase):
    view_name = "acts_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.act = ActFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_all_the_things(self):
        item = ItemFactory()
        other_item = ItemFactory()
        item.acts.set([self.act])
        other_item.acts.set([self.act])
        show = ShowFactory()
        self.act.shows.set([show])
        performer = PerformerFactory()
        self.act.performers.set([performer])
        login_as(self.user, self)
        response = self.client.get(self.url)
        print(response.content)
        self.assertContains(response, "'id': '%d'" % self.act.pk)
        self.assertContains(response, "'title': '%s'" % self.act.title)
        self.assertContains(response, "'num_items': '2'")
        self.assertContains(response, "'num_perf': '1'")
        self.assertContains(
            response,
            "'song_artist': '%s'" % self.act.song_artist)
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
