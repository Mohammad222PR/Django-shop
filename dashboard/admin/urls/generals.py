from django.urls import path
from dashboard.admin.views import generals as views


urlpatterns = [
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
]
