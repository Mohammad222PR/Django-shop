from django.urls import path
from . import views

app_name = "payment"
urlpatterns = [
    path("verify/zarin/", views.PaymentZarinVerifyView.as_view(), name="verify"),
    path("verify/zibal/", views.PaymentZibalVerifyView.as_view(), name="verify"),
    path("verify/novin/", views.PaymentZibalVerifyView.as_view(), name="verify"),

]
