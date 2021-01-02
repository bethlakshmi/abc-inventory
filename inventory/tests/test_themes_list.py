from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    StyleVersionFactory,
    UserFactory
)
from inventory.tests.functions import (
    login_as,
    set_image,
)
from datetime import (
    date,
    timedelta,
)
from inventory.models import StyleVersion


class TestThemesList(TestCase):
    '''Tests for review_costume_list view'''
    view_name = "themes_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.version = StyleVersionFactory(currently_live=True,
                                           currently_test=True)
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.version.name)
        self.assertContains(response, reverse(
            "manage_theme",
            urlconf="inventory.urls",
            args=[self.version.pk]))
        self.assertContains(
            response,
            ('<a href="%s" role="button" class="btn inventory-btn-primary">' +
             'Manage Items</a>') % reverse(
                "items_list",
                urlconf="inventory.urls"),
            html=True)
        self.assertContains(
            response,
            '<i class="inventory-text-success fas fa-check-circle"></i>',
            2)

    def test_list_all_the_things(self):
        boring_version = StyleVersionFactory()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.version.name)
        self.assertContains(response, boring_version.name)
        self.assertContains(
            response,
            '<i class="inventory-text-success fas fa-check-circle"></i>',
            2)
        self.assertContains(response, reverse(
            "manage_theme",
            urlconf="inventory.urls",
            args=[self.version.pk]))
        self.assertContains(response, reverse(
            "manage_theme",
            urlconf="inventory.urls",
            args=[boring_version.pk]))

    def test_list_w_no_items(self):
        StyleVersion.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "List of Themes and Versions")

    def test_show_changed(self):
        login_as(self.user, self)
        response = self.client.get(
            "%s?changed_id=%d" % (self.url, self.version.pk))
        self.assertContains(response, "if (row.id == %d) {" % self.version.pk)
