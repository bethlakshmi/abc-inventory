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
from inventory.models import Subitem


class TestSubItemList(TestCase):
    '''Tests for review_costume_list view'''
    view_name = "subitems_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = SubitemFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_items_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.item.title)
        self.assertContains(response, reverse(
            "item_edit",
            urlconf="inventory.urls",
            args=[self.item.item.pk]))
        self.assertContains(
            response,
            '<a href="%s" class="nav-link active">SubItem List</a>' % (
                self.url),
            html=True)

    def test_list_items_all_the_things(self):
        busy_item = ItemFactory(
            description="description",
            category=CategoryFactory(),
            disposition=DispositionFactory(),
            year="2020",
            subject="Subject",
            note="Note",
            date_acquired=date.today() - timedelta(days=1),
            date_deaccession=date.today(),
            price=12.50)
        self.item = SubitemFactory(
            item=busy_item,
            description="subdescription",
            width=4,
            height=4,
            depth=4,
            )
        busy_item.tags.set([TagFactory()])
        self.item.tags.set([TagFactory()])
        busy_item.connections.set([busy_item])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "'id': '%d'" % self.item.pk)
        self.assertContains(response, "'title': '%s'" % self.item.title)
        self.assertContains(response,
                            "'parent_title': '%s" % busy_item.title)
        self.assertContains(response,
                            "'category': '%s'" % busy_item.category.name)
        self.assertContains(
            response,
            "'disposition': '%s'" % busy_item.disposition.state)
        self.assertContains(response, "'w': '%d'" % self.item.width)
        self.assertContains(response, "'h': '%d'" % self.item.height)
        self.assertContains(response, "'d': '%d'" % self.item.depth)
        self.assertContains(response, "'year': '%s'" % busy_item.year)
        self.assertContains(response, "'subject': '%s'" % busy_item.subject)
        self.assertContains(
            response,
            "'price': '$%s'" % '{0:.2f}'.format(busy_item.price))
        self.assertContains(response,
                            "'description': '%s'" % self.item.description)
        self.assertContains(response,
                            "'item_description': '%s'" % busy_item.description)
        self.assertContains(response, "'note': '%s'" % busy_item.note)
        self.assertContains(
            response,
            "'item_tags': '%s, '" % busy_item.tags.all()[0].name)
        self.assertContains(response,
                            "'tags': '%s, '" % self.item.tags.all()[0].name)
        self.assertContains(response,
                            "'connections': '%s, '" % busy_item.title)
        self.assertContains(
            response,
            "'date_acquired': '%s'" % busy_item.date_acquired.strftime(
                "%B %-d, %Y"))
        self.assertContains(
            response,
            "'date_deaccession': '%s'" % busy_item.date_deaccession.strftime(
                "%B %-d, %Y"))

    def test_list_w_image(self):
        image = ItemImageFactory(item=self.item.item)
        set_image(image)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, image.filer_image)

    def test_list_w_text(self):
        text = ItemTextFactory(item=self.item.item)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, text.text)

    def test_list_w_no_items(self):
        Subitem.objects.all().delete()
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "List of Items")

    def test_show_changed(self):
        login_as(self.user, self)
        response = self.client.get(self.url + "?changed_id=%d" % self.item.pk)
        self.assertContains(response, "if (row.id == %d) {" % self.item.pk)
