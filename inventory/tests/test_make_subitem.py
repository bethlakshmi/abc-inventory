from django.test import TestCase
from django.urls import reverse
from django.test import Client
from inventory.tests.factories import (
    ItemFactory,
    SubitemFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Subitem


class TestMakeSubitem(TestCase):
    '''Tests for subitem create & update'''

    add_name = 'subitem_create'
    update_name = 'subitem_update'
    delete_name = 'subitem_delete'

    def setUp(self):
        self.client = Client()
        self.object = SubitemFactory()
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

    def subitem_data(self):
        return {'title': "New Name",
                'subitem_number': 1,
                'item': ItemFactory().pk}

    def test_create_get(self):
        from inventory.views.default_view_text import make_subitem_messages
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Subitem")
        self.assertContains(response, make_subitem_messages['create_intro'])
        self.assertContains(response, "Title")

    def test_create_post(self):
        from inventory.views.default_view_text import make_subitem_messages
        start = Subitem.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.subitem_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_subitem_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, Subitem.objects.all().count())
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse('subitems_list', urlconf="inventory.urls"),
            self.object.pk+1))

    def test_create_error(self):
        from inventory.views.default_view_text import make_subitem_messages
        data = self.subitem_data()
        data['title'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_subitem_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_subitem_messages['create_intro'])

    def test_edit_get(self):
        from inventory.views.default_view_text import make_subitem_messages
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Subitem")
        self.assertContains(response, make_subitem_messages['edit_intro'])
        self.assertContains(response, "Title")

    def test_edit_post(self):
        from inventory.views.default_view_text import make_subitem_messages
        start = Subitem.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.subitem_data(),
                                    follow=True)
        self.assertContains(
            response,
            make_subitem_messages['edit_success'] % "New Name")
        self.assertEqual(start, Subitem.objects.all().count())
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse('subitems_list', urlconf="inventory.urls"),
            self.object.pk))

    def test_edit_bad_data(self):
        from inventory.views.default_view_text import make_subitem_messages
        data = self.subitem_data()
        data['title'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_subitem_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_subitem_messages['edit_intro'])

    def test_delete_get(self):
        from inventory.views.default_view_text import make_subitem_messages
        response = self.client.get(self.delete_url)
        self.assertContains(response, "Delete Subitem")
        self.assertContains(
            response,
            make_subitem_messages['delete_intro'] % self.object)

    def test_delete_post(self):
        from inventory.views.default_view_text import make_subitem_messages
        start = Subitem.objects.all().count()
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(
            response,
            make_subitem_messages['delete_success'] % self.object)
        self.assertEqual(start-1, Subitem.objects.all().count())
