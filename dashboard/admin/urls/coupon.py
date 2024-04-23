from django.urls import path
from dashboard.admin.views import coupon as views


urlpatterns = [
    path("coupon/list/", views.AdminCouponListView.as_view(), name="coupon-list"),
    path(
        "coupon/update/<int:pk>/",
        views.AdminCouponUpdateView.as_view(),
        name="coupon-update",
    ),
    path("coupon/create/", views.AdminCouponCreateView.as_view(), name="coupon-create"),
    path(
        "coupon/delete/<int:pk>/",
        views.AdminCouponDeleteView.as_view(),
        name="coupon-delete",
    ),
]
