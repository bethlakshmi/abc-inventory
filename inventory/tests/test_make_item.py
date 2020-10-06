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
    assert_option_state,
)
from datetime import (
    date,
    timedelta,
)
from inventory.models import Item


class TestMakeItem(TestCase):
    '''Tests for review_costume_list view'''
    view_name = "item_create"
    edit_name = "item_edit"

    def get_basics(self):
        new_category = CategoryFactory()
        return {
            'step': 0,
            'title':  "New Title",
            'description': "New Description",
            'subject': "New Subject",
            'category': new_category.pk,
        }

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory(
            description="description",
            category=CategoryFactory(),
            disposition=DispositionFactory(),
            year="2020",
            width=2,
            height=2,
            depth=2,
            subject="Subject",
            note="Note",
            date_acquired=date.today(),
            date_deaccession=date.today() - timedelta(days=1),
            price=12.50)
        self.url = reverse(self.view_name, urlconf="inventory.urls")
        self.edit_url = reverse(self.edit_name,
                                urlconf="inventory.urls",
                                args=[self.item.pk])

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_get_create(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "Creating New Item")
        self.assertContains(response, "The Basics")

    def test_get_edit(self):
        login_as(self.user, self)
        response = self.client.get(self.edit_url)
        self.assertContains(response,
                            '<h2 class="subtitle">%s</h2>' % self.item.title)
        self.assertContains(response, "The Basics")
        self.assertContains(response, self.item.description)
        self.assertContains(response, self.item.subject)
        assert_option_state(response,
                            self.item.category.pk,
                            self.item.category.name,
                            True)

    def test_get_edit_bad_id(self):
        self.edit_url = reverse(self.edit_name,
                           urlconf="inventory.urls",
                           args=[self.item.pk+1])
        login_as(self.user, self)
        response = self.client.get(self.edit_url)
        self.assertEqual(404, response.status_code)

    def test_post_basics_create_save_and_continue(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=basics)
        self.assertContains(
            response,
            '<h2 class="subtitle">%s</h2>' % basics['title'])
        self.assertContains(response, "Physical Information")

    def test_post_basics_create_finish(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['finish'] = "Finish"
        response = self.client.post(self.url, data=basics, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % basics['title'])
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk+1))

    def test_post_basics_edit_save_and_continue(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.edit_url, data=basics)
        self.assertContains(
            response,
            '<h2 class="subtitle">%s</h2>' % basics['title'])
        self.assertContains(response, "Physical Information")

    def test_post_basics_edit_finish(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=basics, follow=True)
        self.assertContains(
            response,
            "Updated Item: %s" % basics['title'])
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)

    def test_post_basics_bad_data(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['category'] = basics['category'] + 1
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=basics)
        print(response.content)
        self.assertContains(response, "Creating New Item")
        self.assertContains(response, "There is an error on the form.")
