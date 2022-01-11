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
from inventory.models import Item
from django.test.utils import override_settings


class TestBulkItemUploadTroupe(TestCase):
    ''' This view reuses the generic wizard that is fully tested in
    make_item testing.  As such, this collection limits itself to
    what's special for bulk image upload - including a lot of multi-form
    logic'''
    view_name = "item_upload"
    header_select = '<select name="header_0" id="id_header_0">'

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls")
        login_as(self.user, self)

    @override_settings(INVENTORY_MODE='troupe')
    def test_upload_troupe_mode(self):
        from inventory.views.default_view_text import user_messages
        file1 = open("inventory/tests/no_header.csv", 'rb')
        response = self.client.post(
            self.url,
            data={'new_items': file1,
                  'has_header': False,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        assert_option_state(response, "quantity", "Quantity")
        assert_option_state(response, "size", "Size")
        assert_option_state(response, "last_used", "Last Used")
        self.assertContains(response, 'value="Finish"')
        self.assertContains(response, 'value="Save & Continue >>"')

    @override_settings(INVENTORY_MODE='troupe')
    def test_post_map_troupe_continue(self):
        count = Item.objects.all().count()
        response = self.client.post(
            self.url,
            data={'header_0': '',
                  'header_1': 'title',
                  'header_2': 'quantity',
                  'header_3': 'size',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "3",
                  '0-cell_3': "38B",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  '1-cell_3': "Large",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(response, 'value="Finish"')
        self.assertContains(response, "Performer")
        self.assertContains(response, "Add Additional Item Details")

    @override_settings(INVENTORY_MODE='troupe')
    def test_post_troupe_relations(self):
        working_item = ItemFactory()
        category = CategoryFactory()
        disposition = DispositionFactory()
        tag = TagFactory()
        show = ShowFactory()
        act = ActFactory()
        performer = PerformerFactory()
        color = ColorFactory()
        response = self.client.post(
            self.url,
            data={'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'form-0-id': working_item.id,
                  'form-0-title': working_item.title,
                  'form-0-category': category.pk,
                  'form-0-disposition': disposition.pk,
                  'form-0-tags': [tag.pk],
                  'form-0-shows': [show.pk],
                  'form-0-acts': [act.pk],
                  'form-0-performers': [performer.pk],
                  'form-0-colors': [color.pk],
                  'step': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "Uploaded 1 items.")
        updated_item = Item.objects.get(pk=working_item.pk)
        self.assertEqual(updated_item.category, category)
        self.assertEqual(updated_item.disposition, disposition)
        self.assertEqual(updated_item.shows.first(), show)
        self.assertEqual(updated_item.acts.first(), act)
        self.assertEqual(updated_item.colors.first(), color)
        self.assertEqual(updated_item.performers.first(), performer)
        self.assertEqual(updated_item.tags.first(), tag)
        self.assertRedirects(response,
                             reverse('items_list', urlconf='inventory.urls'))
        self.assertContains(
            response,
            '<a href="/inventory/show/list" class="nav-link ">Shows</a>')

    @override_settings(INVENTORY_MODE='troupe')
    def test_post_troupe_relations_no_title(self):
        working_item = ItemFactory()
        response = self.client.post(
            self.url,
            data={'form-TOTAL_FORMS': 1,
                  'form-INITIAL_FORMS': 1,
                  'form-MIN_NUM_FORMS': 0,
                  'form-MAX_NUM_FORMS': 1000,
                  'forms-0-id': working_item.id,
                  'forms-0-title': working_item.title,
                  'step': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, "This field is required.")
