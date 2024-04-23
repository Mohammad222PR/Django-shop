from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.views.generic import ListView, DetailView

from dashboard.mixins import HasCustomerAccessPermission
from order.models import Order, OrderStatus


class CustomerOrderListView(HasCustomerAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/customer/orders/order-list.html"
    paginate_by = 5
    context_object_name = "orders"

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


class CustomerOrderDetailView(
    HasCustomerAccessPermission, LoginRequiredMixin, DetailView
):
    template_name = "dashboard/customer/orders/order-detail.html"
    context_object_name = "order"

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class CustomerOrderInvoiceDetailView(
    HasCustomerAccessPermission, LoginRequiredMixin, DetailView
):
    template_name = "dashboard/customer/orders/order-invoice.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user, status=OrderStatus.success.value
        )
