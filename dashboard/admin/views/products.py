from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from ..forms.products import ChangeProductDataForm
from dashboard.admin.forms import ProductForm, ProductImageForm
from dashboard.mixins.admin import HasAdminAccessPermission
from shop.models import Product, ProductStatus, ProductCategory, ProductImage
from django.views import View
status = ProductStatus


class AdminProductListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/products/product-list.html"
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


class AdminProductUpdateView(
    HasAdminAccessPermission, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    template_name = "dashboard/admin/products/product-update.html"
    queryset = Product.objects.all()
    form_class = ProductForm
    success_message = "ویرایش محصول با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:product-update", kwargs={"pk": self.get_object().pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = ProductImageForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.product_image.prefetch_related()
        return obj


class AdminProductDeleteView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView
):
    template_name = "dashboard/admin/products/product-delete.html"
    queryset = Product.objects.all()
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "حذف محصول با موفقیت انجام شد"
    context_object_name = "product"


class AdminProductCreateView(
    LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView
):
    template_name = "dashboard/admin/products/product-create.html"
    queryset = Product.objects.all()
    form_class = ProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد"
    context_object_name = "product"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(
            reverse_lazy(
                "dashboard:admin:product-update", kwargs={"pk": form.instance.pk}
            )
        )

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list")


class AdminProductAddImageView(
    LoginRequiredMixin, HasAdminAccessPermission, CreateView
):
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:product-update", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_queryset(self):
        return ProductImage.objects.filter(product__id=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs.get("pk"))
        messages.success(self.request, "تصویر مورد نظر با موفقیت ثبت شد")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "تصویر ارسال نشد لطفا مجدد امتحان نمایید")
        return redirect(
            reverse_lazy(
                "dashboard:admin:product-update", kwargs={"pk": self.kwargs.get("pk")}
            )
        )


class AdminProductImageDeleteView(
    HasAdminAccessPermission, LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    success_message = "تصویر با موفقیت حذف شد"

    def get_queryset(self):
        return ProductImage.objects.filter(product__id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy(
            "dashboard:admin:product-update", kwargs={"pk": self.kwargs.get("pk")}
        )

    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs.get("image_id"))


class AdminChangeProductDataView(LoginRequiredMixin, HasAdminAccessPermission, View):
    def post(self, request):
        form = ChangeProductDataForm(request.POST)
        change_type = form.cleaned_data['change_type']
        percent = form.cleaned_data['percent']
        select_action = form.cleaned_data['select_action']
        if form.is_valid():
            for product_id in select_action:
                try:
                    product = Product.objects.get(id=product_id)
            
                    if change_type == 'increase':
                        product.price += (product.price * percent / 100)
                    elif change_type == 'decrease':
                        product.price -= (product.price * percent / 100)
                    product.save()
                except Product.DoesNotExist:
                    # در صورتی که محصول با این ایدی وجود نداشته باشد
                    # می‌توانید عملیات مناسبی انجام دهید، مانند ایجاد یک لاگ یا ارسال پیام خطا به کاربر
                    pass

        return redirect("dashboard:admin:product-list")
                    
