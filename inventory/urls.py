from django.conf.urls import url
from inventory.views import ItemsListView

app_name = "inventory"

urlpatterns = [
    #  landing page
    url(r'^inventory/?', ItemsListView.as_view(), name='items_list'),
]
