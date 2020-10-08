from django.test import (
    Client,
    TestCase
)
from django.contrib.auth.models import User
from inventory.tests.factories import (
    CategoryFactory,
    DispositionFactory,
    ItemFactory,
    ItemImageFactory,
    ItemTextFactory,
    TagFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from datetime import (
    date,
    timedelta,
)
from django.contrib.admin.sites import AdminSite


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        password = 'mypassword'
        self.privileged_user = User.objects.create_superuser(
            'myuser', 'myemail@test.com', password)
        self.client.login(
            username=self.privileged_user.username,
            password=password)

    def test_get_item(self):
        obj = ItemFactory(
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
        response = self.client.get('/admin/inventory/item/',
                                   follow=True)
        self.assertContains(response, obj.title)
        self.assertContains(
            response,
            '<td class="field-has_label"><img src="/static/admin/img/' +
            'icon-no.svg" alt="False"></td>')
        self.assertContains(
            response,
            '<td class="field-has_image"><img src="/static/admin/img/' +
            'icon-no.svg" alt="False"></td>')

    def test_has_label(self):
        obj = ItemTextFactory()
        response = self.client.get('/admin/inventory/item/',
                                   follow=True)
        self.assertContains(response, obj.item.title)
        self.assertContains(
            response,
            '<td class="field-has_label"><img src="/static/admin/img/' +
            'icon-yes.svg" alt="True"></td>')
        self.assertContains(
            response,
            '<td class="field-has_image"><img src="/static/admin/img/' +
            'icon-no.svg" alt="False"></td>')

    def test_has_image(self):
        obj = ItemImageFactory()
        response = self.client.get('/admin/inventory/item/',
                                   follow=True)
        self.assertContains(response, obj.item.title)
        self.assertContains(
            response,
            '<td class="field-has_label"><img src="/static/admin/img/' +
            'icon-no.svg" alt="False"></td>')
        self.assertContains(
            response,
            '<td class="field-has_image"><img src="/static/admin/img/' +
            'icon-yes.svg" alt="True"></td>')
