from django.conf.urls import url
from inventory.views import (
	ItemsListView,
	MakeItemWizard,
)


app_name = "inventory"

urlpatterns = [
    #  landing page
    url(r'^inventory/item/list/?', ItemsListView.as_view(), name='items_list'),
    url(r'^inventory/item/create/?',
    	MakeItemWizard.as_view(),
    	name='items_create'),
    url(r'^inventory/item/edit/(?P<item_id>\d+)/?',
    	MakeItemWizard.as_view(),
    	name='items_edit'),
]
