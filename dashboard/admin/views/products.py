from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, UpdateView

from dashboard.admin.forms import ProductForm
from dashboard.mixins.dashboard import AdminDashBoardMixin
from shop.models import Product, ProductStatus, ProductCategory

status = ProductStatus


class AdminProductListView(AdminDashBoardMixin, LoginRequiredMixin, ListView):
    template_name = 'dashboard/admin/products/product-list.html'
    context_object_name = "products"
    paginate_by = 7

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = Product.objects.all().distinct()

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


class AdminProductUpdateView(AdminDashBoardMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/products/product-update.html"
    queryset = Product.objects.all()
    form_class = ProductForm
    success_message = "محصول با موفقیت اضافه شد"

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-update', kwargs={'pk': self.get_object().pk})


