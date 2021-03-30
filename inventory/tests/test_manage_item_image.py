from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ItemFactory,
    ItemImageFactory,
    UserFactory
)
from inventory.tests.functions import (
    login_as,
    set_image,
)
from inventory.models import ItemImage
from easy_thumbnails.files import get_thumbnailer


class TestManageItem(TestCase):
    view_name = "manage_item_image"
    options = {'size': (100, 100), 'crop': False}
    image_checkbox = '''<input type="checkbox" name="%s" style="display: none;"
        id="id_%s_%d" value="%d" %s>'''

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        ItemImage.objects.all().delete()
        self.itemimage = ItemImageFactory()
        set_image(self.itemimage)
        self.item = self.itemimage.item
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls",
                           args=[self.item.pk])

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_get_w_image(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(
            self.itemimage.filer_image).get_thumbnail(self.options).url
        self.assertContains(response, "Manage Images for %s" % self.item.title)
        self.assertContains(
            response,
            "<img src='%s' title='Linked to: %s;'/>" % (
                thumb_url,
                self.item.title))
        self.assertContains(
            response,
            self.image_checkbox % (
                "current_images",
                "current_images",
                0,
                self.itemimage.filer_image.pk, 'checked'),
            html=True)
        self.assertContains(
            response,
            'type="checkbox" name="delete_images" value="%d"' % (
                self.itemimage.filer_image.pk))

    def test_get_item_wout_image(self):
        self.item = ItemFactory()
        image = self.itemimage.filer_image
        self.itemimage.delete()
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls",
                           args=[self.item.pk])
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(image).get_thumbnail(self.options).url
        self.assertContains(response, "Manage Images for %s" % self.item.title)
        self.assertContains(
            response,
            "<img src='%s' title='No Item Links'/>" % (thumb_url))
        self.assertContains(
            response,
            self.image_checkbox % (
                "unattached_images",
                "unattached_images",
                0,
                image.pk,
                ''),
            html=True)
        self.assertContains(
            response,
            'type="checkbox" name="delete_images" value="%d"' % (image.pk))

    def test_get_w_image_linked_elsewhere(self):
        self.other_image = ItemImageFactory()
        set_image(self.other_image)
        login_as(self.user, self)
        response = self.client.get(self.url)
        thumb_url = get_thumbnailer(
            self.other_image.filer_image).get_thumbnail(self.options).url
        self.assertContains(response, "Manage Images for %s" % self.item.title)
        self.assertContains(
            response,
            "<img src='%s' title='Linked to: %s;'/>" % (
                thumb_url,
                self.other_image.item.title))
        self.assertContains(
            response,
            self.image_checkbox % (
                "other_images",
                "other_images",
                0,
                self.other_image.filer_image.pk,
                ''),
            html=True)
        self.assertContains(
            response,
            'type="checkbox" name="delete_images" value="%d"' % (
                self.other_image.filer_image.pk))

    def test_get_edit_bad_id(self):
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls",
                           args=[self.item.pk+1])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_post_clear_images(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'current_images': [],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "Updated Item: %s<br>Linked 0 images. Added 0 images." % (
                self.item.title))
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_hacked_buttons(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'current_images': [],
                  'new_images': ""})
        self.assertContains(
            response,
            "Button Click Unclear.  If you did not tamper with the form," +
            " contact us.")

    def test_post_pick_own_image(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'current_images': [self.itemimage.filer_image.pk],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "Updated Item: %s<br>Linked 1 images. Added 0 images." % (
                self.item.title))
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_pick_unlinked_image(self):
        login_as(self.user, self)
        link_me = set_image()

        response = self.client.post(
            self.url,
            data={'unattached_images': [link_me.pk],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "Updated Item: %s<br>Linked 1 images. Added 0 images." % (
                self.item.title))
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_pick_cross_linked_image(self):
        login_as(self.user, self)
        self.other_image = ItemImageFactory()
        set_image(self.other_image)

        response = self.client.post(
            self.url,
            data={'other_images': [self.other_image.filer_image.pk],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            ("Updated Item: %s<br>Linked 1 images. Added 0 images.  " +
             "Unlinked 0 images.") % (self.item.title))
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_unlink_images(self):
        login_as(self.user, self)
        link_me = set_image()

        response = self.client.post(
            self.url,
            data={'current_images': [],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            ("Updated Item: %s<br>Linked 0 images. Added 0 images.  " +
             "Unlinked 1 images.") % (self.item.title))
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))

    def test_post_bad_image_id(self):
        login_as(self.user, self)
        link_me = set_image()
        response = self.client.post(
            self.url,
            data={'current_images': [self.itemimage.filer_image.pk + 100],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "%d is not one of the available choices." % (
                self.itemimage.filer_image.pk + 100))

    def test_post_file_uploads(self):
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("inventory/tests/redexpo.jpg", 'rb')
        file2 = open("inventory/tests/10yrs.jpg", 'rb')
        response = self.client.post(
            self.url,
            data={'current_images': [],
                  'new_images': [file1, file2],
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "Updated Item: %s<br>Linked 0 images. Added 2 images." % (
                self.item.title))

    def test_cancel(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'cancel': "Cancel"},
            follow=True)
        self.assertContains(response, "The last update was canceled.")
        self.assertRedirects(response,
                             reverse("items_list", urlconf="inventory.urls"))

    def test_post_delete_image(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'delete_images': [self.itemimage.filer_image.pk],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(response, "Deleted 1 images.")
        self.assertEqual(self.item.images.count(), 0)
        self.assertContains(response, "if (row.id == %d) {" % (self.item.pk))
