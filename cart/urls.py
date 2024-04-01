from django.urls import path, re_path
from . import views

app_name = "cart"

urlpatterns = [
    # cart urls
    path(
        "session/add-product/",
        views.SessionAddProduct.as_view(),
        name="session-add-product",
    ),
    path(
        "session/cart-summary/",
        views.SessionCartSummaryView.as_view(),
        name="session-cart-summary",
    ),
    path(
        "session/update-product-quantity/",
        views.SessionUpdateProductQuantityView.as_view(),
        name="session-update-product-quantity",
    ),
    path(
        "session/cart-remove-product/",
        views.SessionRemoveProductView.as_view(),
        name="session-remove-product",
    ),
]
