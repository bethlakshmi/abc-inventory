from django.conf.urls import url
from inventory.views import (
	ItemsListView,
	MakeItemWizard,
)


app_name = "inventory"

urlpatterns = [
    #  landing page
    url(r'^inventory/home?', ItemsListView.as_view(), name='items_list'),
    url(r'^inventory/item/create/?',
    	MakeItemWizard.as_view(),
    	name='items_create'),
]
