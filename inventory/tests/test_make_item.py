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

    def get_further(self):
        new_tag = TagFactory()
        other_new_tag = TagFactory()
        return {
            'step': 2,
            'item_id':  self.item.pk,
            'notes': "new notes",
            'tags': (new_tag.pk, other_new_tag.pk),
            'connections': (self.item.pk, ),
        }

    def get_physical(self):
        return {
            'step': 1,
            'item_id':  self.item.pk,
            'height': 1,
            'width': 2,
            'depth': 5.875,
            'year': "c. 2000",
            'date_acquired': "",
            'date_deaccession': "",
            'price': 2.50,
        }

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
            date_acquired=date.today() - timedelta(days=1),
            date_deaccession=date.today(),
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
        self.assertNotContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

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
        self.assertNotContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

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
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

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
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

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
        self.assertContains(response, "Creating New Item")
        self.assertContains(response, "The Basics")
        self.assertContains(response, "There is an error on the form.")
        self.assertNotContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

    def test_post_physical_create_save_and_continue(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(
            response,
            '<h2 class="subtitle">%s</h2>' % self.item.title)
        self.assertContains(response, "<< Back")
        self.assertNotContains(response, "Save & Continue >>")
        self.assertContains(response, "Further Details")

    def test_post_physical_create_finish(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['finish'] = "Finish"
        response = self.client.post(self.url, data=physical, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_physical_edit_save_and_continue(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['date_acquired'] = date.today()
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.edit_url, data=physical)
        self.assertContains(
            response,
            '<h2 class="subtitle">%s</h2>' % self.item.title)
        self.assertContains(response, "<< Back")
        self.assertNotContains(response, "Save & Continue >>")
        self.assertContains(response, "Further Details")

    def test_post_physical_back(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['back'] = "<< Back"
        response = self.client.post(self.edit_url, data=physical)
        self.assertContains(
            response,
            '<h2 class="subtitle">%s</h2>' % self.item.title)
        self.assertNotContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")
        self.assertContains(response, "The Basics")

    def test_post_physical_edit_finish(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['date_deaccession'] = date.today() - timedelta(days=1)
        physical['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=physical, follow=True)
        self.assertContains(
            response,
            "Updated Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)

    def test_post_physical_gone_before_it_came(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['date_acquired'] = date.today()
        physical['date_deaccession'] = date.today() - timedelta(days=1)
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(response, "Physical Information")
        self.assertContains(
            response,
            "The date acquired cannot be AFTER the date of deaccession - " +
            "check these dates and try again.")
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")

    def test_post_further_create_finish(self):
        login_as(self.user, self)
        further = self.get_further()
        further['finish'] = "Finish"
        response = self.client.post(self.url, data=further, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_further_edit_finish(self):
        login_as(self.user, self)
        further = self.get_further()
        further['date_deaccession'] = date.today() - timedelta(days=1)
        further['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=further, follow=True)
        self.assertContains(
            response,
            "Updated Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)

    def test_post_further_back(self):
        login_as(self.user, self)
        further = self.get_further()
        further['back'] = "<< Back"
        response = self.client.post(self.edit_url, data=further, follow=True)
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")
        self.assertContains(response, "Physical Information")

    def test_post_further_bad_tag(self):
        login_as(self.user, self)
        further = self.get_further()
        further['connections'] = (self.item.pk+1)
        further['finish'] = "Finish"
        response = self.client.post(self.url, data=further)
        self.assertContains(response, "Further Details")
        self.assertContains(response, "<< Back")
        self.assertNotContains(response, "Save & Continue >>")

    def test_cancel(self):
        login_as(self.user, self)
        response = self.client.post(
            self.edit_url,
            data={'cancel': "Cancel"},
            follow=True)
        self.assertContains(response, "The last update was canceled.")
        self.assertRedirects(response,
                             reverse("items_list", urlconf="inventory.urls"))
