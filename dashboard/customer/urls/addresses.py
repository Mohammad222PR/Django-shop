from django.urls import path
from dashboard.customer.views import addresses as views

urlpatterns = [
    path("address/list/", views.CustomerAddressListView.as_view(), name="address-list"),
    path("address/create/", views.CustomerAddressCreateView.as_view(), name="address-create"),
    path("address/update/<int:pk>/", views.CustomerAddressUpdateView.as_view(), name="address-update"),
    path("address/delete/<int:pk>/", views.CustomerAddressDeleteView.as_view(), name="address-delete")
]
