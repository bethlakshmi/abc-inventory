from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    StyleVersionFactory,
    UserFactory
)
from inventory.tests.functions import login_as


class TestActivateTheme(TestCase):
    view_name = "activate_theme"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.version = StyleVersionFactory()
        self.active_version = StyleVersionFactory(currently_live=True,
                                                  currently_test=True)
        self.url = reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.version.pk, "live"])
        self.return_url = reverse("themes_list", urlconf="inventory.urls")
        self.title = "List of Themes and Versions"

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_activate_live(self):
        login_as(self.user, self)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s?changed_id=%d" % (
            self.return_url,
            self.version.pk))
        self.assertContains(response, self.title)
        self.assertContains(response, "Activated %s on %s" % (
            self.version,
            "live"))
        self.assertContains(
            response,
            '<a href="%s">' % reverse(
                self.view_name,
                urlconf="inventory.urls",
                args=[self.active_version.pk, "live"]))
        self.assertNotContains(
            response,
            '<a href="%s">' % reverse(
                self.view_name,
                urlconf="inventory.urls",
                args=[self.active_version.pk, "test"]))

    def test_activate_test(self):
        login_as(self.user, self)
        self.url = reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.version.pk, "test"])
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s?changed_id=%d" % (
            self.return_url,
            self.version.pk))
        self.assertContains(response, self.title)
        self.assertContains(response, "Activated %s on %s" % (
            self.version,
            "test"))
        self.assertContains(
            response,
            '<a href="%s">' % reverse(
                self.view_name,
                urlconf="inventory.urls",
                args=[self.active_version.pk, "test"]))
        self.assertNotContains(
            response,
            '<a href="%s">' % reverse(
                self.view_name,
                urlconf="inventory.urls",
                args=[self.active_version.pk, "live"]))

    def test_get_bad_id(self):
        login_as(self.user, self)
        response = self.client.get(reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.active_version.pk+1, "live"]))
        self.assertEqual(404, response.status_code)

    def test_get_bad_system(self):
        login_as(self.user, self)
        response = self.client.get(reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.version.pk, "bad"]))
        self.assertEqual(404, response.status_code)
