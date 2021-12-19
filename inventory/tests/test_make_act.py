from django.test import TestCase
from django.urls import reverse
from django.test import Client
from inventory.tests.factories import (
    ActFactory,
    PerformerFactory,
    ShowFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Act
from datetime import (
    date,
    timedelta,
)


class TestMakeAct(TestCase):
    '''Tests for act manipulation'''

    add_name = 'act_create'
    update_name = 'act_update'
    delete_name = 'act_delete'
    model_class = Act

    def setUp(self):
        self.client = Client()
        self.object = ActFactory()
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

    def data(self):
        performer = PerformerFactory()
        show = ShowFactory()
        return {'title': "New Name",
                'performers': [performer.pk],
                'shows': [show.pk],
                'song': "I put a spell on you",
                'song_artist': "Anyone",
                'notes': "these are notes",
                'first_performed': date.today() - timedelta(days=1),
                'last_performed': date.today()}

    def test_create_get(self):
        from inventory.views.default_view_text import make_act_messages
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, "Create Act")
        self.assertContains(response, make_act_messages['create_intro'])
        self.assertContains(response, "Title")

    def test_create_post(self):
        from inventory.views.default_view_text import make_act_messages
        start = self.model_class.objects.all().count()
        response = self.client.post(self.create_url,
                                    data=self.data(),
                                    follow=True)
        self.assertContains(
            response,
            make_act_messages['create_success'] % "New Name")
        self.assertEqual(start + 1, self.model_class.objects.all().count())

    def test_create_error(self):
        from inventory.views.default_view_text import make_act_messages
        data = self.data()
        data['title'] = ""
        response = self.client.post(self.create_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_act_messages['create_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_act_messages['create_intro'])

    def test_edit_get(self):
        from inventory.views.default_view_text import make_act_messages
        response = self.client.get(self.edit_url)
        self.assertContains(response, "Update Act")
        self.assertContains(response, make_act_messages['edit_intro'])
        self.assertContains(response, "Title")

    def test_edit_post(self):
        from inventory.views.default_view_text import make_act_messages
        start = self.model_class.objects.all().count()
        response = self.client.post(self.edit_url,
                                    data=self.data(),
                                    follow=True)
        self.assertContains(
            response,
            make_act_messages['edit_success'] % "New Name")
        self.assertEqual(start, self.model_class.objects.all().count())

    def test_edit_bad_data(self):
        from inventory.views.default_view_text import make_act_messages
        data = self.data()
        data['title'] = ""
        response = self.client.post(self.edit_url, data=data, follow=True)
        self.assertNotContains(
            response,
            make_act_messages['edit_success'] % "New Name")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, make_act_messages['edit_intro'])

    def test_delete_get(self):
        from inventory.views.default_view_text import make_act_messages
        response = self.client.get(self.delete_url)
        self.assertContains(response, "Delete Act")
        self.assertContains(
            response,
            make_act_messages['delete_intro'] % self.object)

    def test_delete_post(self):
        from inventory.views.default_view_text import make_act_messages
        start = self.model_class.objects.all().count()
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(
            response,
            make_act_messages['delete_success'] % self.object)
        self.assertEqual(start-1, self.model_class.objects.all().count())
