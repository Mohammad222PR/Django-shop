from django.urls import path, re_path
from dashboard.admin.views import products as views


urlpatterns = [
   path("product/list/", views.AdminProductListView.as_view(), name="product-list"),

   path(r"product/update/<int:pk>/", views.AdminProductUpdateView.as_view(), name="product-update")
]
