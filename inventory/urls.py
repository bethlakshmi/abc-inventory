from django.conf.urls import url
from inventory.views import (
    BulkImageUpload,
    ItemsListView,
    MakeItemWizard,
    ManageItemImage,
    ManageTheme,
    SubItemsListView,
    ThemeView,
)


app_name = "inventory"

urlpatterns = [
    url(r'^inventory/(?P<version_id>\d+)/style.css',
        ThemeView.as_view(),
        name='theme_style'),
    url(r'^inventory/style.css', ThemeView.as_view(), name='theme_style'),
    url(r'^inventory/item/list/?', ItemsListView.as_view(), name='items_list'),
    url(r'^inventory/subitem/list/?',
        SubItemsListView.as_view(),
        name='subitems_list'),
    url(r'^inventory/item/create/?',
        MakeItemWizard.as_view(),
        name='item_create'),
    url(r'^inventory/item/edit/(?P<item_id>\d+)/?',
        MakeItemWizard.as_view(),
        name='item_edit'),
    url(r'^inventory/image/upload/?',
        BulkImageUpload.as_view(),
        name='image_upload'),
    url(r'^inventory/item/images/(?P<item_id>\d+)/?',
        ManageItemImage.as_view(),
        name='manage_item_image'),
    url(r'^inventory/style_edit/(?P<version_id>\d+)/?',
        ManageTheme.as_view(),
        name='manage_theme')]
