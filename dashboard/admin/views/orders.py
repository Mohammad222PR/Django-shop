from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from dashboard.admin.forms.orders import OrderForm
from dashboard.mixins import HasAdminAccessPermission
from order.models import Order, OrderStatus


class AdminOrderListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/orders/order-list.html"
    paginate_by = 5
    context_object_name = 'orders'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(id__icontains=search_q)
        if status := self.request.GET.get("status"):
            queryset = queryset.filter(status=status)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["status_types"] = OrderStatus.choices
        return context


class AdminOrderDetailView(HasAdminAccessPermission, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/orders/order-detail.html"
    context_object_name = 'order'
    form_class = OrderForm
    queryset = Order.objects.all()
    success_message = 'با موفقیت انجام شد'

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:order-detail', kwargs={'pk': self.object.pk})


class AdminOrderInvoiceDetailView(HasAdminAccessPermission, LoginRequiredMixin, DetailView):
    template_name = "dashboard/admin/orders/order-invoice.html"
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.all()
