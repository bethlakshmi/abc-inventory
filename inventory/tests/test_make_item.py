from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    CategoryFactory,
    DispositionFactory,
    ItemFactory,
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
from inventory.models import (
    Item,
    ItemText,
)
from django.test.utils import override_settings


class TestMakeItem(TestCase):
    view_name = "item_create"
    edit_name = "item_edit"
    item_id = '<input type="hidden" name="item_id" value="%d" id="id_item_id">'
    title_html = '<h2 class="inventory-title">%s</h2>'

    def get_further(self):
        new_tag = TagFactory()
        other_new_tag = TagFactory()
        return {
            'step': 2,
            'item_id':  self.item.pk,
            'notes': "new notes",
            'tags': (new_tag.pk, other_new_tag.pk),
            'connections': (self.item.pk, ),
            'text': "",
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

    @override_settings(INVENTORY_MODE='museum')
    def test_get_edit_museum(self):
        login_as(self.user, self)
        response = self.client.get(self.edit_url)
        self.assertContains(response, self.title_html % self.item.title)
        self.assertContains(response, "The Basics")
        self.assertContains(response, self.item.description)
        self.assertContains(response, self.item.subject)
        self.assertContains(response, "Subject")
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

    @override_settings(INVENTORY_MODE='museum')
    def test_post_basics_create_save_and_continue(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=basics)
        self.assertContains(response, self.title_html % basics['title'])
        self.assertContains(response, "Physical Information")
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")
        self.assertContains(
            response,
            self.item_id % (self.item.pk + 1),
            html=True)

    @override_settings(INVENTORY_MODE='museum')
    def test_post_basics_create_finish(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['finish'] = "Finish"
        response = self.client.post(self.url, data=basics, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % basics['title'])
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk+1))

    @override_settings(INVENTORY_MODE='museum')
    def test_post_basics_edit_save_and_continue(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.edit_url, data=basics)
        self.assertContains(response, self.title_html % basics['title'])
        self.assertContains(response, "Physical Information")
        self.assertContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")
        self.assertContains(response, self.item_id % self.item.pk, html=True)

    @override_settings(INVENTORY_MODE='museum')
    def test_post_basics_edit_finish(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=basics, follow=True)
        self.assertContains(
            response,
            "Updated Item: %s" % basics['title'])
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)

    @override_settings(INVENTORY_MODE='museum')
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

    @override_settings(INVENTORY_MODE='museum')
    def test_post_physical_create_save_and_continue(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(response, self.title_html % self.item.title)
        self.assertContains(response, "<< Back")
        self.assertNotContains(response, "Save & Continue >>")
        self.assertContains(response, "Proceed to Images >>")
        self.assertContains(response, "Further Details")
        self.assertContains(response, self.item_id % self.item.pk, html=True)
        self.assertContains(
            response,
            '<textarea name="text" cols="40" rows="10" class="user-tiny-mce"' +
            'id="id_text">\n</textarea>',
            html=True)

    @override_settings(INVENTORY_MODE='museum')
    def test_post_physical_create_finish(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['finish'] = "Finish"
        response = self.client.post(self.url, data=physical, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    @override_settings(INVENTORY_MODE='museum')
    def test_post_physical_edit_save_and_continue(self):
        label = ItemTextFactory(item=self.item)
        login_as(self.user, self)
        physical = self.get_physical()
        physical['date_acquired'] = date.today()
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.edit_url, data=physical)
        print(response.content)
        self.assertContains(response, self.title_html % self.item.title)
        self.assertContains(response, "<< Back")
        self.assertNotContains(response, "Save & Continue >>")
        self.assertContains(response, "Proceed to Images >>")
        self.assertContains(response, "Further Details")
        self.assertContains(response, self.item_id % self.item.pk, html=True)
        self.assertContains(
            response,
            '<textarea name="text" cols="40" rows="10" class="user-tiny-mce"' +
            'id="id_text">\n</textarea>',
            html=True)
        self.assertContains(
            response,
            ('<textarea name="%d-text" cols="40" rows="10" ' +
             'class="user-tiny-mce" id="id_%d-text">%s</textarea>') % (
                label.pk,
                label.pk,
                label.text),
            html=True)
        self.assertContains(
            response,
            '<input type="submit" name="add" value="Add Text" class="btn ' +
            'inventory-btn-primary" >',
            html=True)

    def test_post_physical_back(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['back'] = "<< Back"
        response = self.client.post(self.edit_url, data=physical)
        self.assertContains(response, self.title_html % self.item.title)
        self.assertNotContains(response, "<< Back")
        self.assertContains(response, "Save & Continue >>")
        self.assertContains(response, "The Basics")

    @override_settings(INVENTORY_MODE='museum')
    def test_post_physical_edit_finish(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['date_deaccession'] = date.today() - timedelta(days=1)
        physical['finish'] = "Finish"
        with self.settings(INVENTORY_MODE='museum'):
            response = self.client.post(self.edit_url, data=physical, follow=True)
        self.assertContains(
            response,
            "Updated Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)
        self.assertNotContains

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

    def test_post_physical_bad_width(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['width'] = -1
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(response, "Physical Information")
        self.assertContains(
            response,
            "w - Ensure this value is greater than or equal to 0.00.")
        self.assertContains(response, "!&nbsp;&nbsp;Dimensions:")
        self.assertContains(response, "Save & Continue >>")

    def test_post_physical_bad_height(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['height'] = -1
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(response, "Physical Information")
        self.assertContains(
            response,
            "h - Ensure this value is greater than or equal to 0.00.")
        self.assertContains(response, "!&nbsp;&nbsp;Dimensions:")
        self.assertContains(response, "Save & Continue >>")

    def test_post_physical_bad_depth(self):
        login_as(self.user, self)
        physical = self.get_physical()
        physical['depth'] = -1
        physical['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=physical)
        self.assertContains(response, "Physical Information")
        self.assertContains(
            response,
            "d - Ensure this value is greater than or equal to 0.00.")
        self.assertContains(response, "!&nbsp;&nbsp;Dimensions:")
        self.assertContains(response, "Save & Continue >>")

    def test_post_further_create_finish(self):
        login_as(self.user, self)
        further = self.get_further()
        further['finish'] = "Finish"
        response = self.client.post(self.url, data=further, follow=True)
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse("items_list", urlconf="inventory.urls"),
            self.item.pk))
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))
        self.assertNotContains(response, "Text:")

    def test_post_further_create_text(self):
        login_as(self.user, self)
        further = self.get_further()
        further["text"] = "New text for %d" % self.item.pk
        further['finish'] = "Finish"
        response = self.client.post(self.url, data=further, follow=True)
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse("items_list", urlconf="inventory.urls"),
            self.item.pk))
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))
        self.assertContains(response, "<i>Text 1:</i>&nbsp;&nbsp;%s<br>" % (
            further["text"]))

    def test_post_further_edit_finish(self):
        login_as(self.user, self)
        further = self.get_further()
        further['date_deaccession'] = date.today() - timedelta(days=1)
        further['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=further, follow=True)
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse("items_list", urlconf="inventory.urls"),
            self.item.pk))
        self.assertContains(
            response,
            "Updated Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)
        self.assertNotContains(response, "Text:")

    def test_post_further_edit_text(self):
        label = ItemTextFactory(item=self.item)
        login_as(self.user, self)
        further = self.get_further()
        further['date_deaccession'] = date.today() - timedelta(days=1)
        further['%d-text' % label.pk] = "edited text for pk %d" % label.pk
        further['finish'] = "Finish"
        response = self.client.post(self.edit_url, data=further, follow=True)
        self.assertRedirects(response, "%s?changed_id=%s" % (
            reverse("items_list", urlconf="inventory.urls"),
            self.item.pk))
        self.assertContains(
            response,
            "Updated Item: %s" % self.item.title)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)
        self.assertContains(response, "<i>Text 1:</i>&nbsp;&nbsp;%s<br>" % (
            further['%d-text' % label.pk]))
        self.assertNotContains(response, "<i>Text 2:</i>")

    def test_post_further_redirect(self):
        label = ItemTextFactory(item=self.item)
        login_as(self.user, self)
        further = self.get_further()
        further['date_deaccession'] = date.today() - timedelta(days=1)
        further['%d-text' % label.pk] = "edited text for pk %d" % label.pk
        further['redirect'] = "Proceed to Images >>"
        response = self.client.post(self.edit_url, data=further, follow=True)
        self.assertRedirects(response, reverse(
            "manage_item_image",
            urlconf="inventory.urls",
            args=[self.item.pk]))

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
        self.assertContains(response, "Proceed to Images >>")

    def test_cancel(self):
        login_as(self.user, self)
        response = self.client.post(
            self.edit_url,
            data={'cancel': "Cancel"},
            follow=True)
        self.assertContains(response, "The last update was canceled.")
        self.assertRedirects(response,
                             reverse("items_list", urlconf="inventory.urls"))

    def test_bad_button_name(self):
        from inventory.views.default_view_text import user_messages
        login_as(self.user, self)
        response = self.client.post(
            self.edit_url,
            data={'bad_button': "Bad Button"},
            follow=True)
        self.assertContains(
            response,
            user_messages["BUTTON_CLICK_UNKNOWN"]["description"])

        self.assertRedirects(response,
                             reverse('items_list', urlconf='inventory.urls'))

    def test_post_further_add_text(self):
        login_as(self.user, self)
        further = self.get_further()
        further["text"] = "New text for %d" % self.item.pk
        further['add'] = "Add Text"
        response = self.client.post(self.url, data=further, follow=True)
        label = ItemText.objects.get(text=further["text"])
        self.assertContains(response, "Further Details")
        self.assertContains(
            response,
            "Created new text: %s" % further["text"])
        self.assertContains(
            response,
            ('<textarea name="%d-text" cols="40" rows="10" ' +
             'class="user-tiny-mce" id="id_%d-text">%s</textarea>') % (
                label.pk,
                label.pk,
                label.text),
            html=True)
        self.assertContains(
            response,
            '<textarea name="text" cols="40" rows="10" class="user-tiny-mce"' +
            'id="id_text">\n</textarea>',
            html=True)

    def test_post_further_delete_text(self):
        label = ItemTextFactory(item=self.item)
        login_as(self.user, self)
        further = self.get_further()
        further['%d-text' % label.pk] = ""
        further['add'] = "Add Text"
        response = self.client.post(self.url, data=further, follow=True)
        self.assertContains(response, "Further Details")
        self.assertContains(
            response,
            "Deleted a text item")
        self.assertNotContains(
            response,
            ('<textarea name="%d-text" cols="40" rows="10" ' +
             'class="user-tiny-mce" id="id_%d-text">%s</textarea>') % (
                label.pk,
                label.pk,
                label.text),
            html=True)
        self.assertContains(
            response,
            '<textarea name="text" cols="40" rows="10" class="user-tiny-mce"' +
            'id="id_text">\n</textarea>',
            html=True)
