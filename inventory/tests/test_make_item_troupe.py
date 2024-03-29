from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ActFactory,
    PerformerFactory,
    CategoryFactory,
    ColorFactory,
    DispositionFactory,
    ItemFactory,
    ShowFactory,
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
from inventory.models import Item
from django.test.utils import override_settings


class TestMakeItemTroupe(TestCase):
    view_name = "item_create"
    edit_name = "item_edit"
    item_id = '<input type="hidden" name="item_id" value="%d" id="id_item_id">'
    title_html = '<h2 class="inventory-title">%s</h2>'

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
            'sz': ['Lg', ]
        }

    def get_basics(self):
        new_category = CategoryFactory()
        new_color = ColorFactory()
        show = ShowFactory()
        return {
            'step': 0,
            'title':  "New Title",
            'description': "New Description",
            'category': new_category.pk,
            'color': [new_color.pk],
            'shows': [show.pk],
        }

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.item = ItemFactory(
            description="description",
            category=CategoryFactory(),
            disposition=DispositionFactory(),
            width=2,
            height=2,
            depth=2,
            size="all sizes",
            sz=["Sm", ],
            note="Note",
            date_acquired=date.today() - timedelta(days=1),
            date_deaccession=date.today(),
            last_used=date.today(),
            price=12.50)
        self.url = reverse(self.view_name, urlconf="inventory.urls")
        self.edit_url = reverse(self.edit_name,
                                urlconf="inventory.urls",
                                args=[self.item.pk])

    @override_settings(INVENTORY_MODE='troupe')
    def test_post_basics_troupe(self):
        act = ActFactory()
        login_as(self.user, self)
        basics = self.get_basics()
        basics['acts'] = [act.pk]
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.url, data=basics, follow=True)
        updated_item = Item.objects.latest('pk')
        self.assertEqual(updated_item.acts.all().first(), act)
        self.assertContains(response, "Last used")
        self.assertContains(response, "Size")
        self.assertContains(response, "Performers")
        self.assertNotContains(response, "Year")

    @override_settings(INVENTORY_MODE='troupe')
    def test_load_sz(self):
        login_as(self.user, self)
        basics = self.get_basics()
        basics['next'] = "Save & Continue >>"
        response = self.client.post(self.edit_url, data=basics, follow=True)
        self.assertContains(response, "Size")
        self.assertContains(response, "Sz")
        self.assertContains(
            response,
            '<input type="checkbox" name="sz" value="Sm" ' +
            'class="no_bullet_list" id="id_sz_1" checked>',
            html=True)

    @override_settings(INVENTORY_MODE='troupe')
    def test_get_edit_troupe(self):
        login_as(self.user, self)
        with self.settings(INVENTORY_MODE='troupe'):
            response = self.client.get(self.edit_url)
        self.assertContains(response, self.title_html % self.item.title)
        self.assertContains(response, "The Basics")
        self.assertContains(response, "Acts")

    @override_settings(INVENTORY_MODE='troupe')
    def test_post_physical_create_finish(self):
        performer = PerformerFactory()
        login_as(self.user, self)
        physical = self.get_physical()
        physical["performers"] = [performer.pk]
        physical["quantity"] = 1
        physical['finish'] = "Finish"
        response = self.client.post(self.url, data=physical, follow=True)
        self.assertContains(
            response,
            "Created new Item: %s" % self.item.title)
        updated_item = Item.objects.latest('pk')
        self.assertEqual(updated_item.performers.all().first(), performer)
        self.assertNotContains(
            response,
            '<input type="submit" name="add" value="Add Text" class="btn ' +
            'inventory-btn-primary" >',
            html=True)
        self.assertEqual(updated_item.sz_list(), physical['sz'])
