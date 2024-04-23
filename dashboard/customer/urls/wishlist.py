from django.urls import path
from dashboard.customer.views import wishlist as views

urlpatterns = [
    path(
        "wishlist/product/list",
        views.CustomerProductWishlistListView.as_view(),
        name="wishlist-list-product",
    ),
    path(
        "wishlist/product/delete/<int:pk>/",
        views.CustomerWishlistDeleteView.as_view(),
        name="wishlist-delete-product",
    ),
]
