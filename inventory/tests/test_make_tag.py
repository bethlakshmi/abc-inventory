from django.test import TestCase
from django.urls import reverse
from django.test import Client
from inventory.tests.factories import (
    TagFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Tag


class TestMakeTag(TestCase):
    '''Tests for tag create & update'''

    add_name = 'tag_create'
    update_name = 'tag_update'
    delete_name = 'tag_delete'

    def setUp(self):
        self.client = Client()
        self.object = TagFactory()
        self.create_url = reverse(self.add_name,
                                  urlconf='inventory.urls')
        self.edit_url = reverse(self.update_name,
                                args=[self.object.pk],
                                urlconf='inventory.urls')
        self.delete_url = reverse(self.delete_name,
                                  args=[self.object.pk],
                                  urlconf='inventory.urls')

        user = UserFactory()
        login_as(user, self)

    def tag_data(self):
        return {'name': "New Name",
                'help_text': "Help Text"}

    def test_create_get(self):
        from inventory.views.default_view_text import make_tag_messages
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Tag")
        self.assertContains(response, make_tag_messages['create_intro'])
        self.assertContains(response, "Name")

    def test_create_post(self):
        from inventory.views.default_view_text import make_tag_messages
        start = Tag.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.tag_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_tag_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, Tag.objects.all().count())

    def test_create_error(self):
        from inventory.views.default_view_text import make_tag_messages
        data = self.tag_data()
        data['name'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_tag_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_tag_messages['create_intro'])

    def test_edit_get(self):
        from inventory.views.default_view_text import make_tag_messages
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Tag")
        self.assertContains(response, make_tag_messages['edit_intro'])
        self.assertContains(response, "Name")

    def test_edit_post(self):
        from inventory.views.default_view_text import make_tag_messages
        start = Tag.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.tag_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_tag_messages['edit_success'] % "New Name")
        self.assertEqual(start, Tag.objects.all().count())

    def test_edit_bad_data(self):
        from inventory.views.default_view_text import make_tag_messages
        data = self.tag_data()
        data['name'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_tag_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_tag_messages['edit_intro'])

    def test_delete_get(self):
        from inventory.views.default_view_text import make_tag_messages
        response = self.client.get(self.delete_url)
        self.assertContains(response, "Delete Tag")
        self.assertContains(
            response,
            make_tag_messages['delete_intro'] % self.object)

    def test_delete_post(self):
        from inventory.views.default_view_text import make_tag_messages
        start = Tag.objects.all().count()
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(
            response,
            make_tag_messages['delete_success'] % self.object)
        self.assertEqual(start-1, Tag.objects.all().count())
