from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    CategoryFactory,
    ItemFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Category


class TestMergeCategories(TestCase):
    view_name = "category_merge"
    m_check = (
        '<input type="checkbox" name="categories" value="%d" ' +
        'id="id_categories_%d">')
    m_hidden = (
        '<input type="hidden" name="categories" value="%d" ' +
        'id="id_categories_%d">')

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")
        self.category = CategoryFactory()
        self.category2 = CategoryFactory()
        self.item = ItemFactory(category=self.category)
        self.item2 = ItemFactory(category=self.category2)


    def test_get(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "Pick Categories to Merge")
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category2.name)
        self.assertContains(
            response,
            self.m_check % (self.category.pk, 0),
            html=True)
        self.assertContains(
            response,
            self.m_check % (self.category2.pk, 1),
            html=True)

    def test_post_less_categories(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'categories': [self.category.pk],
                  'step': 0,
                  'next': 'Merge'},
            follow=True)
        self.assertContains(
            response,
            "At least 2 choices are needed for a merge")

    def test_post_good_first_step(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'categories': [self.category.pk, self.category2.pk],
                  'step': 0,
                  'next': 'Merge'},
            follow=True)
        self.assertContains(
            response,
            "Select Category Name")
        self.assertContains(
            response,
            ('<select name="category" id="id_category"><option value="%d">' +
             '%s</option><option value="%d">%s</option></select>') % (
             self.category.pk,
             self.category.name,
             self.category2.pk,
             self.category2.name),
            html=True)
        self.assertContains(
            response,
            self.m_hidden % (self.category2.pk, 1),
            html=True)
        self.assertContains(
            response,
            self.m_hidden % (self.category2.pk, 1),
            html=True)

    def test_post_good_merge_items(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'categories': [self.category.pk, self.category2.pk],
                  'category': self.category.pk,
                  'step': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Merged 2 categories, re-categorized 1 items to %s." % (
                self.category.name))

    def test_post_bad_category(self):
        login_as(self.user, self)
        bad_category = CategoryFactory()
        response = self.client.post(
            self.url,
            data={'categories': [self.category.pk, self.category2.pk],
                  'category': bad_category.pk,
                  'step': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Select a valid choice.")
        self.assertNotContains(
            response,
            '<option value="%d">%s</option>' % (bad_category.pk,
                                                bad_category.name))
