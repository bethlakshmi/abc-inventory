from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import UserFactory
from inventory.tests.functions import login_as
from inventory.models import Item


class TestBulkItemUpload(TestCase):
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

    def test_get(self):
        from inventory.forms.default_form_text import item_upload_help
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, item_upload_help['has_header'])
        self.assertContains(
            response,
            user_messages['BULK_FILE_UPLOAD_INSTRUCTIONS']['description'])
        self.assertNotContains(response, 'value="Finish"')

    def test_upload_no_header(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        file1 = open("inventory/tests/no_header.csv", 'rb')
        response = self.client.post(
            self.url,
            data={'new_items': file1,
                  'has_header': False,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(
            response,
            'Preview Item Upload &amp; Select Column Mapping')
        self.assertContains(
            response,
            user_messages['SETUP_ITEM_UPLOAD_INSTRUCTIONS']['description'])
        self.assertContains(
            response,
            self.header_select)
        self.assertContains(
            response,
            '<input type="text" name="0-cell_0" value="12/28/20" ' +
            'id="id_0-cell_0">',
            html=True)
        self.assertContains(response, 'value="Finish"')
        self.assertNotContains(response, 'value="Save & Continue >>"')

    def test_upload_with_header(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        file1 = open("inventory/tests/with_header.csv", 'rb')
        response = self.client.post(
            self.url,
            data={'new_items': file1,
                  'has_header': True,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(
            response,
            'Preview Item Upload &amp; Select Column Mapping')
        self.assertContains(
            response,
            user_messages['SETUP_ITEM_UPLOAD_INSTRUCTIONS']['description'])
        self.assertContains(
            response,
            self.header_select)
        self.assertContains(response, '<tr class="inventory-table-header">')
        self.assertContains(
            response,
            '<input type="text" name="0-cell_0" value="12/28/20" ' +
            'id="id_0-cell_0">',
            html=True)

    def test_post_map_date(self):
        count = Item.objects.all().count()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': 'date_acquired',
                  'header_1': 'title',
                  'header_2': '',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "blah",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "blah",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertRedirects(response,
                             reverse('items_list', urlconf='inventory.urls'))
        self.assertContains(response, "Uploaded 2 items.")
        self.assertEqual(count + 2, Item.objects.all().count())

    def test_post_map_price(self):
        count = Item.objects.all().count()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': '',
                  'header_1': 'title',
                  'header_2': 'price',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "3.33",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertRedirects(response,
                             reverse('items_list', urlconf='inventory.urls'))
        self.assertContains(response, "Uploaded 2 items.")
        self.assertEqual(count + 2, Item.objects.all().count())

    def test_post_map_dimensions(self):
        count = Item.objects.all().count()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': 'width',
                  'header_1': 'title',
                  'header_2': 'height',
                  '0-cell_0': '1.2',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "2.3",
                  '0-cell_3': "4.5",
                  '1-cell_0': '',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "",
                  '1-cell_3': "",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertRedirects(response,
                             reverse('items_list', urlconf='inventory.urls'))
        self.assertContains(response, "Uploaded 2 items.")
        self.assertEqual(count + 2, Item.objects.all().count())
        self.assertContains(response, "2.3", 1)

    def test_post_bad_meta_data(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': '',
                  'header_1': 'title',
                  'header_2': 'price',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "3.33",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  'step': 1,
                  'num_rows': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            user_messages['NO_FORM_ERROR']['description'])

    def test_post_no_title(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': '',
                  'header_1': '',
                  'header_2': 'price',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "3.33",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response,
                            "One column must be labeled as the title.")
        self.assertContains(
            response,
            'Preview Item Upload &amp; Select Column Mapping')
        self.assertContains(
            response,
            "There is an error on the form.")

    def test_post_bad_price(self):
        from inventory.forms.default_form_text import item_format_error
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': '',
                  'header_1': 'title',
                  'header_2': 'price',
                  '0-cell_0': '12/28/20',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "bad",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, item_format_error['price'], 1)
        self.assertContains(
            response,
            'Preview Item Upload &amp; Select Column Mapping')
        self.assertContains(
            response,
            "There is an error on the form.")

    def test_post_bad_date(self):
        from inventory.forms.default_form_text import item_format_error
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'header_0': 'date_acquired',
                  'header_1': 'title',
                  'header_2': 'price',
                  '0-cell_0': 'Dec 28, 2020',
                  '0-cell_1': "Title 1",
                  '0-cell_2': "3.33",
                  '1-cell_0': '2/28/20',
                  '1-cell_1': "Title 2",
                  '1-cell_2': "5",
                  'step': 1,
                  'num_rows': 2,
                  'num_cols': 3,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(response, item_format_error['date_acquired'], 1)
        self.assertContains(
            response,
            'Preview Item Upload &amp; Select Column Mapping')

    def test_upload_not_csv(self):
        from inventory.forms.default_form_text import item_upload_help
        login_as(self.user, self)
        file1 = open("inventory/tests/not_csv", 'rb')
        response = self.client.post(
            self.url,
            data={'new_items': file1,
                  'has_header': False,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(response, item_upload_help['has_header'])
        self.assertContains(
            response,
            "Allowed extensions are: csv.")

    def test_upload_bad_rows(self):
        from inventory.forms.default_form_text import item_upload_help
        login_as(self.user, self)
        file1 = open("inventory/tests/bad_number_cells.csv", 'rb')
        response = self.client.post(
            self.url,
            data={'new_items': file1,
                  'has_header': False,
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(response, item_upload_help['has_header'])
        self.assertContains(
            response,
            'Irregular number of columns, the delimiter is a comma (,) and ' +
            'the quote is a double quote (&quot;), this is likely an ' +
            'encoding problem.')
