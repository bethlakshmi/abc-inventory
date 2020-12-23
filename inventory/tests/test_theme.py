from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    CategoryFactory,
    DispositionFactory,
    ItemFactory,
    ItemImageFactory,
    ItemTextFactory,
    TagFactory,
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
from inventory.models import Item


class TestTheme(TestCase):
    view_name = "theme_style"

    def setUp(self):
        self.client = Client()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_migrations(self):
        response = self.client.get(self.url)
        self.assertContains(
            response,
            ".inventory-alert-success {")
        self.assertContains(
            response,
            "    background-color: #d4edda;")
        self.assertContains(
            response,
            "    border-color: #c3e6cb;")
        self.assertContains(
            response,
            "    color: #155724;")
        self.assertContains(
            response,
            "}")
