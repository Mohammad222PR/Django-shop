from django.urls import path
from dashboard.customer.views import generals as views


urlpatterns = [
    path("home/", views.CustomerDashBoardHomeView.as_view(), name="home"),
]
