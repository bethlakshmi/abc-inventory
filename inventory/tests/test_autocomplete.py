from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ActFactory,
    CategoryFactory,
    ColorFactory,
    DispositionFactory,
    ItemFactory,
    PerformerFactory,
    ShowFactory,
    TagFactory,
    UserFactory
)
from inventory.tests.functions import login_as


class TestAutoComplete(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_list_categories(self):
        category = CategoryFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('category-autocomplete'))
        self.assertContains(response, category.name)
        self.assertContains(response, category.pk)

    def test_no_access_categories(self):
        category = CategoryFactory()
        response = self.client.get(reverse('category-autocomplete'))
        self.assertNotContains(response, category.name)
        self.assertNotContains(response, category.pk)

    def test_list_categories_w_search_critieria(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('category-autocomplete'),
            category1.name))
        self.assertContains(response, category1.name)
        self.assertContains(response, category1.pk)
        self.assertNotContains(response, category2.name)

    def test_list_dispositions(self):
        disposition = DispositionFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('disposition-autocomplete'))
        self.assertContains(response, disposition.state)
        self.assertContains(response, disposition.pk)

    def test_no_access_dispositions(self):
        disposition = DispositionFactory()
        response = self.client.get(reverse('disposition-autocomplete'))
        self.assertNotContains(response, disposition.state)
        self.assertNotContains(response, disposition.pk)

    def test_list_dispositions_w_search_critieria(self):
        disposition = DispositionFactory()
        disposition2 = DispositionFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('disposition-autocomplete'),
            disposition.state))
        self.assertContains(response, disposition.state)
        self.assertContains(response, disposition.pk)
        self.assertNotContains(response, disposition2.state)

    def test_list_tags(self):
        tag = TagFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('tag-autocomplete'))
        self.assertContains(response, tag.name)
        self.assertContains(response, tag.pk)

    def test_no_access_tags(self):
        tag = TagFactory()
        response = self.client.get(reverse('tag-autocomplete'))
        self.assertNotContains(response, tag.name)
        self.assertNotContains(response, tag.pk)

    def test_list_tags_w_search_critieria(self):
        tag = TagFactory()
        tag2 = TagFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('tag-autocomplete'),
            tag.name))
        self.assertContains(response, tag.name)
        self.assertContains(response, tag.pk)
        self.assertNotContains(response, tag2.name)

    def test_list_connections(self):
        item = ItemFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('connection-autocomplete'))
        self.assertContains(response, item.title)
        self.assertContains(response, item.pk)

    def test_no_access_connections(self):
        item = ItemFactory()
        response = self.client.get(reverse('connection-autocomplete'))
        self.assertNotContains(response, item.title)
        self.assertNotContains(response, item.pk)

    def test_list_tags_w_search_connections(self):
        item = ItemFactory()
        item2 = ItemFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('connection-autocomplete'),
            item.title))
        self.assertContains(response, item.title)
        self.assertContains(response, item.pk)
        self.assertNotContains(response, item2.title)

    def test_list_performers(self):
        performer = PerformerFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('performer-autocomplete'))
        self.assertContains(response, performer.name)
        self.assertContains(response, performer.pk)

    def test_no_access_performers(self):
        performer = PerformerFactory()
        response = self.client.get(reverse('performer-autocomplete'))
        self.assertNotContains(response, performer.name)
        self.assertNotContains(response, performer.pk)

    def test_list_performers_w_search_critieria(self):
        performer = PerformerFactory()
        performer2 = PerformerFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('performer-autocomplete'),
            performer.name))
        self.assertContains(response, performer.name)
        self.assertContains(response, performer.pk)
        self.assertNotContains(response, performer2.name)

    def test_list_acts(self):
        act = ActFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('act-autocomplete'))
        self.assertContains(response, act.title)
        self.assertContains(response, act.pk)

    def test_no_access_acts(self):
        act = ActFactory()
        response = self.client.get(reverse('act-autocomplete'))
        self.assertNotContains(response, act.title)
        self.assertNotContains(response, act.pk)

    def test_list_acts_w_search_critieria(self):
        act = ActFactory()
        act2 = ActFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('act-autocomplete'),
            act.title))
        self.assertContains(response, act.title)
        self.assertContains(response, act.pk)
        self.assertNotContains(response, act2.title)

    def test_list_shows(self):
        show = ShowFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('show-autocomplete'))
        self.assertContains(response, show.title)
        self.assertContains(response, show.pk)

    def test_no_access_shows(self):
        show = ShowFactory()
        response = self.client.get(reverse('show-autocomplete'))
        self.assertNotContains(response, show.title)
        self.assertNotContains(response, show.pk)

    def test_list_shows_w_search_critieria(self):
        show = ShowFactory()
        show2 = ShowFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('show-autocomplete'),
            show.title))
        self.assertContains(response, show.title)
        self.assertContains(response, show.pk)
        self.assertNotContains(response, show2.title)

    def test_list_colors(self):
        obj = ColorFactory()
        login_as(self.user, self)
        response = self.client.get(reverse('color-autocomplete'))
        self.assertContains(response, obj.name)
        self.assertContains(response, obj.pk)

    def test_no_access_colors(self):
        obj = ColorFactory()
        response = self.client.get(reverse('color-autocomplete'))
        self.assertNotContains(response, obj.name)
        self.assertNotContains(response, obj.pk)

    def test_list_colors_w_search_critieria(self):
        obj = ColorFactory()
        obj2 = ColorFactory()
        login_as(self.user, self)
        response = self.client.get("%s?q=%s" % (
            reverse('color-autocomplete'),
            obj.name))
        self.assertContains(response, obj.name)
        self.assertContains(response, obj.pk)
        self.assertNotContains(response, obj2.name)
