from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from inventory.tests.factories import (
    CategoryFactory,
    DispositionFactory,
    ItemFactory,
    TagFactory,
    UserFactory
)
from inventory.tests.functions import login_as
from datetime import (
    date,
    timedelta,
)


class TestItemList(TestCase):
    '''Tests for review_costume_list view'''
    view_name = "items_list"

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")

    def test_list_items_basic(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.item.title)
        self.assertContains(response, reverse(
            "items_edit",
            urlconf="inventory.urls",
            args=[self.item.pk]))

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
            date_acquired=date.today(),
            date_deaccession=date.today() - timedelta(days=1),
            price=12.50)
        busy_item.tags.set([TagFactory()])
        busy_item.connections.set([self.item])
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, reverse(
            "items_edit",
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
                "%b. %-d, %Y"))
        self.assertContains(
            response,
            "'date_deaccession': '%s'" % busy_item.date_deaccession.strftime(
                "%b. %-d, %Y"))
        #self.assertContains(response, "'images': ''" % busy_item.)
        #self.assertContains(response, "'texts': ''" % busy_item.)

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, 
                             "/login/?next=/inventory/item/list",
                             fetch_redirect_response=False)

