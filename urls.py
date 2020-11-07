# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from inventory.views import (
    CategoryAutocomplete,
    DispositionAutocomplete,
)


urlpatterns = [
    # add your own patterns here
    url(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(create_field='name'),
        name='category-autocomplete',
    ),
    url(
        r'^disposition-autocomplete/$',
        DispositionAutocomplete.as_view(create_field='state'),
        name='disposition-autocomplete',
    ),    url(r'^', include('inventory.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
