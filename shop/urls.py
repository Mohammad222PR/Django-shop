from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # product list & retriv & delete & update
    path('product/grid', views.ProductGridView.as_view(), name='product-grid')
]
