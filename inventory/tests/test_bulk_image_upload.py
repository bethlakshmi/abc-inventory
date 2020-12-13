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
    set_image
)
from inventory.models import ItemImage
from easy_thumbnails.files import get_thumbnailer
from filer.models import Image


class TestBulkImageUpload(TestCase):
    ''' This view reuses the generic wizard that is fully tested in 
    make_item testing.  As such, this collection limits itself to 
    what's special for bulk image upload - including a lot of multi-form
    logic'''
    view_name = "image_upload"
    options = {'size': (100, 100), 'crop': False}
    image_checkbox = '''<input type="checkbox" name="current_images"
        style="display: none;" id="id_current_images_%d" value="%d" %s>'''

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.itemimage = ItemImageFactory()
        set_image(self.itemimage)
        self.url = reverse(self.view_name,
                           urlconf="inventory.urls")

    def test_get(self):
        from inventory.forms import item_image_help
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, item_image_help['new_images'])

    def test_upload_files_no_step_error(self):
        from inventory.views import user_messages
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("inventory/tests/redexpo.jpg", 'rb')
        file2 = open("inventory/tests/10yrs.jpg", 'rb')
        response = self.client.post(
            self.url,
            data={'new_images': [file1, file2],
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(
            response,
            user_messages["STEP_ERROR"]["description"])

    def test_upload_files_continue(self):
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("inventory/tests/redexpo.jpg", 'rb')
        file2 = open("inventory/tests/10yrs.jpg", 'rb')
        response = self.client.post(
            self.url,
            data={'new_images': [file1, file2],
                  'step': 0,
                  'next': 'Save & Continue >>'},
            follow=True)
        self.assertContains(
            response,
            "Connect Images to Items")
        image2 = Image.objects.latest('pk')
        image1 = Image.objects.get(pk=image2.pk-1)
        thumb_url = get_thumbnailer(
            image1).get_thumbnail(self.options).url
        self.assertContains(
            response,
            "<img src='%s' title='%s'/>" % (
                thumb_url,
                image1))
        thumb_url = get_thumbnailer(
            image2).get_thumbnail(self.options).url
        self.assertContains(
            response,
            "<img src='%s' title='%s'/>" % (
                thumb_url,
                image2))

'''
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
            self.image_checkbox % (0, image.pk, ''),
            html=True)

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

    def test_post_pick_loaded_images(self):
        login_as(self.user, self)
        link_me = set_image()

        response = self.client.post(
            self.url,
            data={'current_images': [self.itemimage.filer_image.pk,
                                     link_me.pk],
                  'new_images': "",
                  'finish': 'Save'},
            follow=True)
        self.assertContains(
            response,
            "Updated Item: %s<br>Linked 2 images. Added 0 images." % (
                self.item.title))
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


    def test_cancel(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'cancel': "Cancel"},
            follow=True)
        self.assertContains(response, "The last update was canceled.")
        self.assertRedirects(response,
                             reverse("items_list", urlconf="inventory.urls"))
'''
