from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import ValidationError, FieldError
from django.shortcuts import render, get_object_or_404
from django.views import generic
from faker.utils.text import slugify
from typing import Any
from cart.cart import CartSession
from shop.models import Product, ProductStatus, ProductCategory

# Create your views here.
status = ProductStatus


class ProductGridView(generic.ListView):
    template_name = "shop/product-grid.html"
    context_object_name = "products"
    paginate_by = 7

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = Product.objects.filter(status=status.published.value).distinct()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q).distinct()
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id).distinct()
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price).distinct()
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price).distinct()
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by).distinct()
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = Product.objects.filter(
            status=status.published.value
        ).count()
        context["categories"] = ProductCategory.objects.all().distinct()
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "shop/product-detail.html"
    context_object_name = "product"
