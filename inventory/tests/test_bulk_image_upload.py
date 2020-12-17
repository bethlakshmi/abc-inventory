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
        from inventory.forms.default_form_text import item_image_help
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, item_image_help['new_images'])

    def test_upload_files_missing_step_error(self):
        from inventory.views.default_view_text import user_messages
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
        print(response.content)
        image2 = Image.objects.latest('pk')
        image1 = Image.objects.get(pk=image2.pk-1)
        thumb_url = get_thumbnailer(
            image1).get_thumbnail(self.options).url
        self.assertContains(
            response,
            "Connect Images to Items")
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
        self.assertContains(
            response,
            '<input type="hidden" name="step" value="1" id="id_step">',
            html=True)
        self.assertContains(
            response,
            '<input type="hidden" name="association_count" value="2" ' +
            'id="id_association_count">',
            html=True)

    def test_upload_files_finish(self):
        UserFactory(username='admin_img')
        login_as(self.user, self)
        file1 = open("inventory/tests/redexpo.jpg", 'rb')
        file2 = open("inventory/tests/10yrs.jpg", 'rb')
        response = self.client.post(
            self.url,
            data={'new_images': [file1, file2],
                  'step': 0,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Uploaded 2 images.<br>Attached 0 images.")

    def test_post_attachments(self):
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-filer_image': img1.pk,
                  '1-filer_image': img2.pk,
                  '0-item': item.pk,
                  '1-item': "",
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Uploaded 2 images.<br>Attached 1 images.")

    def test_post_attachments_bad_item(self):
        # This is legit if a user selects something that is then deleted
        # before they submit
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-filer_image': img1.pk,
                  '1-filer_image': img2.pk,
                  '0-item': item.pk+1,
                  '1-item': "",
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "That choice is not one of the available choices.")

    def test_post_attachments_bad_image(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-filer_image': img1.pk+100,
                  '1-filer_image': img2.pk,
                  '0-item': item.pk,
                  '1-item': "",
                  'step': 1,
                  'association_count': 2,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "There is an error on the form.",
            1)

    def test_post_attachments_bad_association(self):
        # The user would have to be hacking the form to do this.
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-filer_image': img1.pk,
                  '1-filer_image': img2.pk,
                  '0-item': item.pk,
                  '1-item': "",
                  'step': 1,
                  'association_count': 4,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "There is an error on the form.",
            2)

    def test_post_attachments_invalid_association(self):
        # The user would have to be hacking the form to do this.
        from inventory.views.default_view_text import user_messages
        img1 = set_image(self.itemimage)
        img2 = set_image(self.itemimage)
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'0-filer_image': img1.pk,
                  '1-filer_image': img2.pk,
                  '0-item': item.pk,
                  '1-item': "",
                  'step': 1,
                  'association_count': -1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            user_messages["NO_FORM_ERROR"]["description"])
