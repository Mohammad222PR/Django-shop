from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
    path("security-edit/", views.AdminSecurityEditView.as_view(), name="security-edit"),
    path("profile-edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),

]
