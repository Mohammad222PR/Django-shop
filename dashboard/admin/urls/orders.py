from django.urls import path
from dashboard.admin.views import orders as views


urlpatterns = [
    path("orders/list/", views.AdminOrderListView.as_view(), name="order-list"),
    path(
        "orders/detail/<int:pk>/",
        views.AdminOrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "orders/invoice/<int:pk>/",
        views.AdminOrderInvoiceDetailView.as_view(),
        name="order-invoice",
    ),
]
