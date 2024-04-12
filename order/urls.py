from django.urls import path
from . import views

app_name = "order"
urlpatterns = [
    path("checkout/", views.CheckOutOrderView.as_view(), name="checkout"),
    path("completed/", views.OrderCompletedView.as_view(), name="order-completed"),
    path("failed/", views.OrderFaliedView.as_view(), name="order-faild"),
    path("validate-coupon/", views.ValidateCouponView.as_view(), name="validate-coupon"),

]
