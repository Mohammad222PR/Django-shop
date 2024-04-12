from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from dashboard.admin.forms.coupon import CouponValidationForm
from dashboard.mixins import HasAdminAccessPermission
from order.models import Coupon


class AdminCouponListView(HasAdminAccessPermission, LoginRequiredMixin, ListView):
    template_name = 'dashboard/admin/coupon/coupon-list.html'
    context_object_name = 'coupons'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        queryset = Coupon.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(code__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context


class AdminCouponCreateView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'dashboard/admin/coupon/coupon-create.html'
    context_object_name = 'coupon'
    form_class = CouponValidationForm
    queryset = Coupon.objects.all()
    success_message = 'کد تخفیف با موفقیت ساخته شد'

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:coupon-update', kwargs={'pk': self.object.pk})


class AdminCouponUpdateView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/admin/coupon/coupon-update.html'
    context_object_name = 'coupon'
    form_class = CouponValidationForm
    queryset = Coupon.objects.all()
    success_message = 'کد تخفیف با موفقیت بروز رسانی شد'

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:coupon-update', kwargs={'pk': self.object.pk})


class AdminCouponDeleteView(HasAdminAccessPermission, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'dashboard/admin/coupon/coupon-delete.html'
    context_object_name = 'coupon'
    queryset = Coupon.objects.all()
    success_message = 'کد تخفیف با موفقیت حذف شد'

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:coupon-list')

