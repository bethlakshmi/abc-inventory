from django.conf.urls import url
from inventory.views import (
    ItemsListView,
    ManageItemImage,
    MakeItemWizard,
)


app_name = "inventory"

urlpatterns = [
    url(r'^inventory/item/list/?', ItemsListView.as_view(), name='items_list'),
    url(r'^inventory/item/create/?',
        MakeItemWizard.as_view(),
        name='item_create'),
    url(r'^inventory/item/edit/(?P<item_id>\d+)/?',
        MakeItemWizard.as_view(),
        name='item_edit'),
    url(r'^inventory/item/images/(?P<item_id>\d+)/?',
        ManageItemImage.as_view(),
        name='manage_item_image'),
]
