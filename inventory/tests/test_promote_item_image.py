from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ItemImageFactory,
    UserFactory
)
from inventory.tests.functions import (
    login_as,
    set_image,
)


class TestPromoteItemImage(TestCase):
    view_name = "promote_item_image"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.image = ItemImageFactory()
        set_image(self.image)
        self.url = reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.image.pk])
        self.return_url = reverse("items_list", urlconf="inventory.urls")

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_promote(self):
        self.image_orig_main = ItemImageFactory()
        set_image(self.image_orig_main)
        login_as(self.user, self)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s?changed_id=%d" % (
            self.return_url,
            self.image.item.pk))
        self.assertContains(
            response,
            "Set Main Image for %s to image file %s" % (
                self.image.item,
                self.image.filer_image))
        self.assertContains(response, reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.image_orig_main.pk]))

    def test_promote_bad_id(self):
        login_as(self.user, self)
        response = self.client.get(reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.image.pk+1]))
        self.assertEqual(404, response.status_code)
