from django.test import TestCase
from django.urls import reverse
from django.test import Client
from inventory.tests.factories import (
    ItemFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Item


class TestDeleteItem(TestCase):
    '''Tests for subitem create & update'''

    delete_name = 'item_delete'

    def setUp(self):
        self.client = Client()
        self.object = ItemFactory()
        self.delete_url = reverse(self.delete_name,
                                  args=[self.object.pk],
                                  urlconf='inventory.urls')
        user = UserFactory()
        login_as(user, self)

    def test_delete_get(self):
        from inventory.views.default_view_text import delete_item_messages
        response = self.client.get(self.delete_url)
        self.assertContains(response, "Delete Item")
        self.assertContains(
            response,
            delete_item_messages['delete_intro'] % self.object)

    def test_delete_post(self):
        from inventory.views.default_view_text import delete_item_messages
        start = Item.objects.all().count()
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(
            response,
            delete_item_messages['delete_success'] % self.object)
        self.assertEqual(start-1, Item.objects.all().count())
