from django.urls import path

from . import views

app_name = "support"

urlpatterns = [
    path("home/", views.SupportDashBoardHomeView.as_view(), name="home"),

]
