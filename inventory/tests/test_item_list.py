from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from inventory.tests.factories import (
    ItemFactory,
    UserFactory
)
from inventory.tests.functions import login_as


class TestItemList(TestCase):
    '''Tests for review_costume_list view'''
    view_name = "items_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_items_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.item.title)
