from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ActFactory,
    CategoryFactory,
    ColorFactory,
    DispositionFactory,
    ItemFactory,
    PerformerFactory,
    ShowFactory,
    TagFactory,
    UserFactory,
)
from inventory.tests.functions import (
    assert_option_state,
    login_as,
)
from inventory.views.default_view_text import edit_size_messages


class TestBulkItemUploadTroupe(TestCase):
    ''' This view reuses the generic wizard that is fully tested in
    make_item testing.  As such, this collection limits itself to
    what's special for bulk image upload - including a lot of multi-form
    logic'''
    view_name = "bulk_size"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls")
        self.item = ItemFactory(
            description="description",
            category=CategoryFactory(),
            disposition=DispositionFactory(),
            width=2,
            height=2,
            depth=2,
            size="all sizes",
            note="Note",
            price=12.50)
        login_as(self.user, self)

    def test_get(self):
        self.item_w_sz = ItemFactory(
            description="description",
            category=CategoryFactory(),
            disposition=DispositionFactory(),
            width=2,
            height=2,
            depth=2,
            size="all sizes",
            sz='["Sm", "Lg"]',
            note="Note",
            price=12.50)
        self.item_no_size = ItemFactory()
        response = self.client.get(self.url)
        self.assertContains(response, self.item.title)
        self.assertNotContains(response, self.item_w_sz.title)
        self.assertNotContains(response, self.item_no_size.title)
        self.assertContains(
            response, 
            '<input type="checkbox" name="form-0-sz" value="Sm" class=' +
            '"no_bullet_list" id="id_form-0-sz_1">')

    def test_post_success(self):
        response = self.client.post(
            self.url,
            data={'form-0-sz': ['Sm'],
                  'id_form-0-size': 'Small',
                  'form-0-id': self.item.id,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': 'Submit'},
            follow=True)
        self.assertContains(response, edit_size_messages['success'])

    def test_post_success_bad_id(self):
        response = self.client.post(
            self.url,
            data={'form-0-sz': ['Sm'],
                  'id_form-0-size': 'Small',
                  'form-0-id': self.item.id+100,
                  'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'submit': 'Submit'},
            follow=True)
        self.assertNotContains(response, edit_size_messages['success'])
        self.assertContains(response, 'class="inventory-table-error"')
