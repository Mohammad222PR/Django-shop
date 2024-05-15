from django.urls import path
from dashboard.admin.views import chart as views


urlpatterns = [
    path("charts/", views.AdminChartOrderView.as_view(), name="charts"),
]
