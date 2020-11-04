# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from inventory.views import CategoryAutocomplete


urlpatterns = [
    # add your own patterns here
    url(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete',
    ),
    url(r'^', include('inventory.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
