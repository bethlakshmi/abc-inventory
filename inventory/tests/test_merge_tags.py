from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    ItemFactory,
    SubitemFactory,
    TagFactory,
    UserFactory,
)
from inventory.tests.functions import login_as
from inventory.models import Tag


class TestMergeTags(TestCase):
    view_name = "tag_merge"
    m_check = '<input type="checkbox" name="tags" value="%d" id="id_tags_%d">'
    m_hidden = '<input type="hidden" name="tags" value="%d" id="id_tags_%d">'

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse(self.view_name, urlconf="inventory.urls")
        self.item = ItemFactory()
        self.item2 = ItemFactory()
        self.tag = TagFactory()
        self.tag2 = TagFactory()
        self.item.tags.set([self.tag])
        self.item2.tags.set([self.tag2])

    def test_get(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "Pick Tags to Merge")
        self.assertContains(response, self.tag.name)
        self.assertContains(response, self.tag2.name)
        self.assertContains(
            response,
            self.m_check % (self.tag.pk, 0),
            html=True)
        self.assertContains(
            response,
            self.m_check % (self.tag2.pk, 1),
            html=True)

    def test_post_less_tags(self):
        login_as(self.user, self)

        response = self.client.post(
            self.url,
            data={'tags': [self.tag.pk],
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
            data={'tags': [self.tag.pk, self.tag2.pk],
                  'step': 0,
                  'next': 'Merge'},
            follow=True)
        self.assertContains(
            response,
            "Select Tag Name")
        self.assertContains(
            response,
            ('<select name="tag" id="id_tag"><option value="%d">' +
             '%s</option><option value="%d">%s</option></select>') % (
             self.tag.pk,
             self.tag.name,
             self.tag2.pk,
             self.tag2.name),
            html=True)
        self.assertContains(
            response,
            self.m_hidden % (self.tag2.pk, 1),
            html=True)
        self.assertContains(
            response,
            self.m_hidden % (self.tag2.pk, 1),
            html=True)

    def test_post_bad_tag(self):
        login_as(self.user, self)
        bad_tag = TagFactory()
        response = self.client.post(
            self.url,
            data={'tags': [self.tag.pk, self.tag2.pk],
                  'tag': bad_tag.pk,
                  'step': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Select a valid choice.")
        self.assertNotContains(
            response,
            '<option value="%d">%s</option>' % (bad_tag.pk, bad_tag.name))

    def test_post_good_merge_subitems(self):
        login_as(self.user, self)
        self.subitem = SubitemFactory()
        self.subitem2 = SubitemFactory()
        self.subitem.tags.set([self.tag])
        self.subitem2.tags.set([self.tag2])
        response = self.client.post(
            self.url,
            data={'tags': [self.tag.pk, self.tag2.pk],
                  'tag': self.tag.pk,
                  'step': 1,
                  'finish': 'Finish'},
            follow=True)
        self.assertContains(
            response,
            "Merged 2 tags, re-tagged 1 items and 1 subitems to %s." % (
                self.tag.name))
