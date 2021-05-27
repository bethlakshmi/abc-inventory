from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    CategoryFactory,
    DispositionFactory,
    ItemFactory,
    ItemImageFactory,
    ItemTextFactory,
    SubitemFactory,
    TagFactory,
    UserFactory
)
from inventory.tests.functions import (
    login_as,
    set_image,
)
from datetime import (
    date,
    timedelta,
)
from inventory.models import Item


class TestItemList(TestCase):
    view_name = "items_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_with_subitems(self):
        subitem = SubitemFactory()
        tag = TagFactory()
        subitem.tags.set([tag])
        subitem_w_dim = SubitemFactory(width=1, height=2.2, depth=0.001)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            '<td>%s</td><td>%s</td><td>N/A</td><td>%s, </td>' % (
                subitem.title,
                subitem.description,
                tag.name))
        self.assertContains(
            response,
            '<td>%s</td><td>%s</td><td>1.000 X 2.200 X 0.001</td><td></td>' % (
                subitem_w_dim.title,
                subitem_w_dim.description))
        self.assertContains(
            response,
            reverse('subitem_update',
                    urlconf="inventory.urls",
                    args=[subitem_w_dim.pk]))
        self.assertContains(
            response,
            reverse('subitem_create', urlconf="inventory.urls"))

    def test_list_items_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.item.title)
        self.assertContains(response, reverse(
            "item_edit",
            urlconf="inventory.urls",
            args=[self.item.pk]))
        self.assertContains(response, reverse(
            "item_delete",
            urlconf="inventory.urls",
            args=[self.item.pk]))
        self.assertContains(response, reverse(
            "manage_item_image",
            urlconf="inventory.urls",
            args=[self.item.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">Item List</a>' % (
                self.url),
            html=True)

    def test_list_items_all_the_things(self):
        busy_item = ItemFactory(
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
        busy_item.tags.set([TagFactory()])
        busy_item.connections.set([self.item])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, reverse(
            "item_edit",
            urlconf="inventory.urls",
            args=[busy_item.pk]))
        self.assertContains(response, "'id': '%d'" % busy_item.pk)
        self.assertContains(response, "'title': '%s'" % busy_item.title)
        self.assertContains(response,
                            "'category': '%s'" % busy_item.category.name)
        self.assertContains(
            response,
            "'disposition': '%s'" % busy_item.disposition.state)
        self.assertContains(response, "'w': '%d'" % busy_item.width)
        self.assertContains(response, "'h': '%d'" % busy_item.height)
        self.assertContains(response, "'d': '%d'" % busy_item.depth)
        self.assertContains(response, "'year': '%s'" % busy_item.year)
        self.assertContains(response, "'subject': '%s'" % busy_item.subject)
        self.assertContains(
            response,
            "'price': '$%s'" % '{0:.2f}'.format(busy_item.price))
        self.assertContains(response,
                            "'description': '%s'" % busy_item.description)
        self.assertContains(response, "'note': '%s'" % busy_item.note)
        self.assertContains(response,
                            "'tags': '%s, '" % busy_item.tags.all()[0].name)
        self.assertContains(response,
                            "'connections': '%s, '" % self.item.title)
        self.assertContains(
            response,
            "'date_acquired': '%s'" % busy_item.date_acquired.strftime(
                "%B %-d, %Y"))
        self.assertContains(
            response,
            "'date_deaccession': '%s'" % busy_item.date_deaccession.strftime(
                "%B %-d, %Y"))
        self.assertContains(
            response,
            "'updated': '%s by ---'" % busy_item.updated_at.strftime(
                "%B %-d, %Y"))

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_list_w_image_no_main(self):
        image = ItemImageFactory(item=self.item)
        set_image(image)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, image.filer_image, 4)
        self.assertContains(response, reverse(
            "promote_item_image",
            urlconf="inventory.urls",
            args=[image.pk]), 2)

    def test_list_w_image_w_main(self):
        image = ItemImageFactory(item=self.item, main_image=True)
        image2 = ItemImageFactory(item=self.item)
        set_image(image)
        set_image(image2)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, image.filer_image.url, 4)
        self.assertContains(response, image2.filer_image.url, 2)
        self.assertNotContains(response, reverse(
            "promote_item_image",
            urlconf="inventory.urls",
            args=[image.pk]))

    def test_list_w_text(self):
        text = ItemTextFactory(item=self.item)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, text.text)

    def test_list_w_no_items(self):
        Item.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "List of Items")

    def test_show_changed(self):
        login_as(self.user, self)
        response = self.client.get(self.url + "?changed_id=%d" % self.item.pk)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)

    def test_show_error(self):
        login_as(self.user, self)
        response = self.client.get(self.url + "?error_id=%d" % self.item.pk)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)
