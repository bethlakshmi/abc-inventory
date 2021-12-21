# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from inventory.views import (
    ActAutocomplete,
    CategoryAutocomplete,
    ColorAutocomplete,
    ConnectionAutocomplete,
    DispositionAutocomplete,
    PerformerAutocomplete,
    ShowAutocomplete,
    TagAutocomplete,
)


urlpatterns = [
    # add your own patterns here
    url(
        r'^act-autocomplete/$',
        ActAutocomplete.as_view(),
        name='act-autocomplete',
    ),
    url(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(create_field='name'),
        name='category-autocomplete',
    ),
    url(
        r'^color-autocomplete/$',
        ColorAutocomplete.as_view(create_field='name'),
        name='color-autocomplete',
    ),
    url(
        r'^connection-autocomplete/$',
        ConnectionAutocomplete.as_view(),
        name='connection-autocomplete',
    ),
    url(
        r'^disposition-autocomplete/$',
        DispositionAutocomplete.as_view(create_field='state'),
        name='disposition-autocomplete',
    ),
    url(
        r'^performer-autocomplete/$',
        PerformerAutocomplete.as_view(),
        name='performer-autocomplete',
    ),
    url(
        r'^show-autocomplete/$',
        ShowAutocomplete.as_view(),
        name='show-autocomplete',
    ),
    url(
        r'^tag-autocomplete/$',
        TagAutocomplete.as_view(create_field='name'),
        name='tag-autocomplete',
    ),
    url(r'^', include('inventory.urls')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
