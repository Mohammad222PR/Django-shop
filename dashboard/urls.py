from django.urls import path, include

from . import views

app_name = "dashboard"

urlpatterns = [
    path("home/", views.DashBoardHomeView.as_view(), name="home"),
    path("admin/", include("dashboard.admin.urls", namespace="admin")),
    path("customer/", include("dashboard.customer.urls", namespace="customer")),
    path("support/", include("dashboard.support.urls", namespace="support")),
]
