from django.urls import path
from dashboard.customer.views import orders as views

urlpatterns = [
    path("orders/list/", views.CustomerOrderListView.as_view(), name="order-list"),
    path(
        "orders/detail/<int:pk>/",
        views.CustomerOrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "orders/invoice/<int:pk>/",
        views.CustomerOrderInvoiceDetailView.as_view(),
        name="order-invoice",
    ),
    path(
        "orders/re_order/<int:pk>/",
        views.CustomerOrderReOrderView.as_view(),
        name="re-order",
    )
]
