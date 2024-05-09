from django.urls import path, re_path
from dashboard.admin.views import products as views


urlpatterns = [
    path("product/list/", views.AdminProductListView.as_view(), name="product-list"),
    path(
        "product/create/", views.AdminProductCreateView.as_view(), name="product-create"
    ),
    path(
        "product/<int:pk>/delete/",
        views.AdminProductDeleteView.as_view(),
        name="product-delete",
    ),
    path(
        "product/update/<int:pk>/",
        views.AdminProductUpdateView.as_view(),
        name="product-update",
    ),
    path(
        "product/add-image/<int:pk>/",
        views.AdminProductAddImageView.as_view(),
        name="product-add-image",
    ),
    path(
        "product/<int:pk>/remove-image/<int:image_id>/",
        views.AdminProductImageDeleteView.as_view(),
        name="product-remove-image",
    ),
    path(
        "product/change/",
        views.AdminChangeProductDataView.as_view(),
        name="prodcut-change",
    ),
]
