from django.urls import path, re_path
from . import views

app_name = "cart"

urlpatterns = [
    # cart urls
    path(
        "add-product/",
        views.SessionAddProduct.as_view(),
        name="add-product",
    ),
    path(
        "cart-summary/",
        views.SessionCartSummaryView.as_view(),
        name="cart-summary",
    ),
    path(
        "update-product-quantity/",
        views.SessionUpdateProductQuantityView.as_view(),
        name="update-product-quantity",
    ),
    path(
        "cart-remove-product/",
        views.SessionRemoveProductView.as_view(),
        name="remove-product",
    ),
]
