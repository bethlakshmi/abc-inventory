from django.conf.urls import url
from inventory.views import (
    ActivateTheme,
    BulkImageUpload,
    BulkItemUpload,
    CategoryCreate,
    CategoryListView,
    CategoryUpdate,
    CloneTheme,
    DeleteTheme,
    ItemsListView,
    MakeItemWizard,
    ManageItemImage,
    ManageTheme,
    PreviewTheme,
    PromoteItemImage,
    SubitemCreate,
    SubItemsListView,
    SubitemUpdate,
    TagCreate,
    TagDelete,
    TagListView,
    TagUpdate,
    ThemeView,
    ThemesListView,
)


app_name = "inventory"

urlpatterns = [
    url(r'^inventory/(?P<version_id>\d+)/style.css',
        ThemeView.as_view(),
        name='theme_style'),
    url(r'^inventory/style.css', ThemeView.as_view(), name='theme_style'),
    url(r'^inventory/item/list/?', ItemsListView.as_view(), name='items_list'),
    url(r'^inventory/theme/list/?',
        ThemesListView.as_view(),
        name='themes_list'),
    url(r'^inventory/subitem/list/?',
        SubItemsListView.as_view(),
        name='subitems_list'),
    url(r'^inventory/category/list/?',
        CategoryListView.as_view(),
        name='categories_list'),

    url(r'^inventory/item/create/?',
        MakeItemWizard.as_view(),
        name='item_create'),
    url(r'^inventory/item/edit/(?P<item_id>\d+)/?',
        MakeItemWizard.as_view(),
        name='item_edit'),
    url(r'^inventory/image/upload/?',
        BulkImageUpload.as_view(),
        name='image_upload'),
    url(r'^inventory/item/upload/?',
        BulkItemUpload.as_view(),
        name='item_upload'),
    url(r'^inventory/image/promote/(?P<itemimage_id>\d+)/?',
        PromoteItemImage.as_view(),
        name='promote_item_image'),
    url(r'^inventory/item/images/(?P<item_id>\d+)/?',
        ManageItemImage.as_view(),
        name='manage_item_image'),
    url(r'^inventory/activate/(?P<version_id>\d+)/(?P<target_system>[-\w]+)/?',
        ActivateTheme.as_view(),
        name='activate_theme'),
    url(r'^inventory/preview/(?P<version_id>\d+)/?',
        PreviewTheme.as_view(),
        name='preview_theme'),
    url(r'^inventory/preview/?',
        PreviewTheme.as_view(),
        name='preview_off'),
    url(r'^inventory/style_edit/(?P<version_id>\d+)/?',
        ManageTheme.as_view(),
        name='manage_theme'),
    url(r'^inventory/style_delete/(?P<version_id>\d+)/?',
        DeleteTheme.as_view(),
        name='delete_theme'),
    url(r'^inventory/style_clone/(?P<version_id>\d+)/?',
        CloneTheme.as_view(),
        name='clone_theme'),
    url(r'^inventory/category/create/?',
        CategoryCreate.as_view(),
        name='category_create'),
    url(r'^inventory/category/update/(?P<pk>.*)/$',
        CategoryUpdate.as_view(),
        name='category_update'),

    # Tags
    url(r'^inventory/tag/list/?',
        TagListView.as_view(),
        name='tags_list'),
    url(r'^inventory/tag/create/?', TagCreate.as_view(), name='tag_create'),
    url(r'^inventory/tag/delete/(?P<pk>.*)/$',
        TagDelete.as_view(),
        name='tag_delete'),
    url(r'^inventory/tag/update/(?P<pk>.*)/$',
        TagUpdate.as_view(),
        name='tag_update'),

    # Subitems
    url(r'^inventory/subitem/create/?',
        SubitemCreate.as_view(),
        name='subitem_create'),
    url(r'^inventory/subitem/update/(?P<pk>.*)/$',
        SubitemUpdate.as_view(),
        name='subitem_update'),
    ]
