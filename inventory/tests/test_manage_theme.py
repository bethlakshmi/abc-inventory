from django.test import TestCase
from django.test import Client
from django.urls import reverse
from inventory.tests.factories import (
    StyleValueFactory,
    StyleVersionFactory,
    UserFactory
)
from inventory.tests.functions import login_as


class TestManageTheme(TestCase):
    view_name = "manage_theme"
    px_input = ('<input type="number" name="%d-value_%d" value="%d" required' +
                ' id="id_%d-value_%d">')

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.value = StyleValueFactory()
        self.url = reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.value.style_version.pk])
        self.title = "Manage Styles Settings for {}, version {:.1f}".format(
            self.value.style_version.name,
            self.value.style_version.number)
        self.style_url = reverse(
            "theme_style",
            urlconf="inventory.urls",
            args=[self.value.style_version.pk])

    def test_no_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             "/login/?next=%s" % self.url,
                             fetch_redirect_response=False)

    def test_get(self):
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, self.title)
        self.assertContains(response, self.value.value)
        self.assertContains(response,
                            self.value.style_property.selector)
        self.assertContains(response,
                            self.value.style_property.selector.used_for)
        self.assertContains(response,
                            self.value.style_property.style_property)
        self.assertContains(response, self.style_url)
        self.assertContains(response, reverse(
            "clone_theme",
            urlconf="inventory.urls",
            args=[self.value.style_version.pk]))

    def test_get_empty(self):
        empty = StyleVersionFactory()
        login_as(self.user, self)
        response = self.client.get(reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[empty.pk]))
        self.assertContains(
            response,
            "Manage Styles Settings for %s, version %d" % (
                empty.name,
                empty.number))
        self.assertContains(response, reverse(
            "theme_style",
            urlconf="inventory.urls",
            args=[empty.pk]))

    def test_get_bad_id(self):
        login_as(self.user, self)
        response = self.client.get(reverse(
            self.view_name,
            urlconf="inventory.urls",
            args=[self.value.style_version.pk+1]))
        self.assertEqual(404, response.status_code)

    def test_post_finish(self):
        login_as(self.user, self)
        response = self.client.post(self.url, data={
            '%s-value_0' % self.value.pk: "rgba(255,255,255,0)",
            '%s-style_property' % self.value.pk: self.value.style_property.pk,
            'finish': "Finish",
            }, follow=True)
        self.assertContains(
            response,
            "Updated %s" % self.value.style_version)
        self.assertRedirects(response, "%s?changed_id=%d" % (
            reverse('themes_list', urlconf='inventory.urls'),
            self.value.style_version.pk))

    def test_post_update(self):
        login_as(self.user, self)
        response = self.client.post(self.url, data={
            '%s-value_0' % self.value.pk: "rgba(255,255,255,0)",
            '%s-style_property' % self.value.pk: self.value.style_property.pk,
            'update': "Update",
            }, follow=True)
        self.assertContains(response, self.title)
        self.assertContains(
            response,
            "Updated %s" % self.value.style_version)
        self.assertContains(response, 'rgba(255,255,255,0)')
        self.assertContains(response,
                            self.value.style_property.selector)
        self.assertContains(response,
                            self.value.style_property.selector.used_for)
        self.assertContains(response,
                            self.value.style_property.style_property)
        self.assertContains(response, self.style_url)

    def test_cancel(self):
        login_as(self.user, self)
        response = self.client.post(
            self.url,
            data={'cancel': "Cancel"},
            follow=True)
        self.assertContains(response, "The last update was canceled.")
        self.assertRedirects(response,
                             reverse("themes_list", urlconf="inventory.urls"))

    def test_post_bad_data(self):
        login_as(self.user, self)
        response = self.client.post(self.url, data={
            'finish': "Finish",
            }, follow=True)
        self.assertContains(response, self.title)
        self.assertContains(
            response,
            "Something was wrong, correct the errors below and try again.")
        self.assertContains(response, "This field is required.")
        self.assertContains(response, self.style_url)

    def test_get_complicated_property(self):
        from inventory.forms.default_form_text import style_value_help
        complex_value = StyleValueFactory(
            value="5px 4px 3px rgba(10,10,10,1)",
            style_property__style_property="text-shadow",
            style_property__value_type="px px px rgba",
            style_property__selector=self.value.style_property.selector,
            style_version=self.value.style_version)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 0, 5, complex_value.pk, 0),
            html=True)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 1, 4, complex_value.pk, 1),
            html=True)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 2, 3, complex_value.pk, 2),
            html=True)
        self.assertContains(response,
                            complex_value.style_property.selector)
        self.assertContains(response,
                            complex_value.style_property.style_property)
        self.assertContains(response, reverse(
            "clone_theme",
            urlconf="inventory.urls",
            args=[self.value.style_version.pk]))
        self.assertContains(response, style_value_help["text-shadow-0"])
        self.assertContains(response, style_value_help["text-shadow-1"])
        self.assertContains(response, style_value_help["text-shadow-2"])
        self.assertContains(response, style_value_help["text-shadow-3"])

    def test_get_complicated_messed_up_property(self):
        from inventory.forms.default_form_text import theme_help
        complex_value = StyleValueFactory(
            value="5px 4px rgba(10,10,10,1)",
            style_property__value_type="px px px rgba",
            style_property__selector=self.value.style_property.selector,
            style_version=self.value.style_version)
        login_as(self.user, self)
        response = self.client.get(self.url)
        self.assertContains(response, "%s, VALUES: %s" % (
            theme_help['mismatch'],
            "[\'5px\', \'4px\', \'rgba(10,10,10,1)\']"))

    def test_post_complicated_property(self):
        complex_value = StyleValueFactory(
            value="5px 4px 3px rgba(10,10,10,1)",
            style_property__value_type="px px px rgba",
            style_property__selector=self.value.style_property.selector,
            style_version=self.value.style_version)
        login_as(self.user, self)
        response = self.client.post(self.url, data={
            '%s-value_0' % self.value.pk: "rgba(255,255,255,0)",
            '%s-style_property' % self.value.pk: self.value.style_property.pk,
            '%s-value_0' % complex_value.pk: "0",
            '%s-style_property' % (
                complex_value.pk): complex_value.style_property.pk,
            '%s-value_1' % complex_value.pk: "10",
            '%s-value_2' % complex_value.pk: "15",
            '%s-value_3' % complex_value.pk: "rgba(50,50,50,0.5)",
            'update': "Update",
            }, follow=True)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 0, 0, complex_value.pk, 0),
            html=True)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 1, 10, complex_value.pk, 1),
            html=True)
        self.assertContains(
            response,
            self.px_input % (complex_value.pk, 2, 15, complex_value.pk, 2),
            html=True)
        self.assertContains(response, "rgba(50,50,50,0.5)")
        self.assertContains(response,
                            complex_value.style_property.selector)
        self.assertContains(response,
                            complex_value.style_property.style_property)
        self.assertContains(response, reverse(
            "clone_theme",
            urlconf="inventory.urls",
            args=[self.value.style_version.pk]))

    def test_post_complicated_messed_up_property(self):
        from inventory.forms.default_form_text import theme_help
        complex_value = StyleValueFactory(
            value="5px 4px 3px",
            style_property__value_type="px px px rgba",
            style_property__selector=self.value.style_property.selector,
            style_version=self.value.style_version)
        login_as(self.user, self)
        response = self.client.post(self.url, data={
            '%s-value_0' % self.value.pk: "rgba(255,255,255,0)",
            '%s-style_property' % self.value.pk: self.value.style_property.pk,
            '%s-value_0' % complex_value.pk: "0",
            '%s-style_property' % (
                complex_value.pk): complex_value.style_property.pk,
            '%s-value_1' % complex_value.pk: "10",
            '%s-value_2' % complex_value.pk: "15",
            '%s-value_3' % complex_value.pk: "rgba(50,50,50,0.5)",
            'update': "Update",
            }, follow=True)
        self.assertContains(response, "%s, VALUES: %s" % (
            theme_help['mismatch'],
            "[\'5px\', \'4px\', \'3px\']"))
        self.assertContains(
            response,
            "Something was wrong, correct the errors below and try again.")
