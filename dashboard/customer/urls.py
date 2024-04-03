from django.urls import path

from . import views

app_name = "customer"

urlpatterns = [
    path("home/", views.CustomerDashBoardHomeView.as_view(), name="home"),
    path("security-edit/", views.CustomerSecurityEditView.as_view(), name="security-edit")

]
