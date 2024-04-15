from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from dashboard.mixins import HasCustomerAccessPermission
from order.models import Order


class CustomerOrderListView(HasCustomerAccessPermission, LoginRequiredMixin, ListView):
    template_name = "dashboard/customer/orders/order-list.html"
    paginate_by = 5
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_order'] = self.get_queryset().count()
        return context


class CustomerOrderDetailView(HasCustomerAccessPermission, LoginRequiredMixin, DetailView):
    template_name = "dashboard/customer/orders/order-detail.html"
    context_object_name = 'order'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset
