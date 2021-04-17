from django.test import TestCase
from django.urls import reverse
from django.test import Client
from inventory.tests.factories import (
    CategoryFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Category


class TestMakeCategory(TestCase):
    '''Tests for category create & update'''

    add_name = 'category_create'
    update_name = 'category_update'

    def setUp(self):
        self.client = Client()
        self.object = CategoryFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='inventory.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='inventory.urls')
        user = UserFactory()
        login_as(user, self)

    def category_data(self):
        return {'name': "New Name",
                'help_text': "Help Text"}

    def test_create_get(self):
        from inventory.views.default_view_text import make_category_messages
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Category")
        self.assertContains(response, make_category_messages['create_intro'])
        self.assertContains(response, "Name")

    def test_create_post(self):
        from inventory.views.default_view_text import make_category_messages
        start = Category.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.category_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_category_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, Category.objects.all().count())

    def test_create_error(self):
        from inventory.views.default_view_text import make_category_messages
        data = self.category_data()
        data['name'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_category_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_category_messages['create_intro'])

    def test_edit_get(self):
        from inventory.views.default_view_text import make_category_messages
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Category")
        self.assertContains(response, make_category_messages['edit_intro'])
        self.assertContains(response, "Name")

    def test_edit_post(self):
        from inventory.views.default_view_text import make_category_messages
        start = Category.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.category_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_category_messages['edit_success'] % "New Name")
        self.assertEqual(start, Category.objects.all().count())

    def test_edit_bad_data(self):
        from inventory.views.default_view_text import make_category_messages
        data = self.category_data()
        data['name'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_category_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_category_messages['edit_intro'])
