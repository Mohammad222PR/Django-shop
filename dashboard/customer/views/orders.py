from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.views.generic import ListView, DetailView, View
from order.forms import CheckOutOrderForm
from order.models import UserAddress, Order, OrderItem, Coupon
from order.permissions import HasCustomerAccessPermission
from payment.models import PaymentZarin, PaymentZibal
from payment.novin_pay import NovinoPay
from payment.zarinpal_client import ZarinPalSandbox
from payment.zibal_client import Zibal
from dashboard.mixins import HasCustomerAccessPermission
from order.models import Order, OrderStatus
from django.shortcuts import redirect
from django.contrib import messages


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


class CustomerOrderReOrderView(HasCustomerAccessPermission, LoginRequiredMixin, View):
    def get(self, request, pk):
        order_obj = Order.objects.get(id=pk)
        if not order_obj:
            messages.error(request, "این سفارش وجود ندارد")
            return redirect(request.META.get("HTTP_REFERER"))
        for item in order_obj.order_items.all():
            if item.product.stock < item.quantity:
                messages.error(request, "تعدداد انتخوابی از موجودی انبار بیشتر است")
                return redirect(self.request.META.get("HTTP_REFERER"))
        order = self.create_order(order_obj)
        self.create_order_items(order, order_obj)
        order.total_price = order_obj.total_price
        order.save()
        if order_obj.payment_zarin:
            return redirect(self.create_payment_zarinpal_url(order))
        if order_obj.payment_zibal:
            return redirect(self.create_payment_zibal_url(order))
        if order_obj.payment_novin:
            return redirect(self.create_payment_novin_url(order))

    def create_payment_zibal_url(self, order):
        zibal = Zibal()
        response = zibal.payment_request(order.get_price())
        payment_obj = PaymentZibal.objects.create(
            trackId=str(response.get("trackId")), amount=order.get_price()
        )
        order.payment_zibal = payment_obj
        order.save()
        return zibal.generate_payment_url(response.get("trackId"))

    def create_payment_novin_url(self, order):
        novin = NovinoPay()
        response = novin.payment_request(order.get_price())
        payment_obj = PaymentZarin.objects.create(
            authority_id=response.get("authority"), amount=order.get_price()
        )
        order.payment_novin = payment_obj
        order.save()
        return novin.generate_payment_url(response.get("authority"))

    def create_payment_zarinpal_url(self, order):
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request(order.get_price())
        payment_obj = PaymentZarin.objects.create(
            authority_id=response.get("Authority"), amount=order.get_price()
        )
        order.payment_zarin = payment_obj
        order.save()
        return zarinpal.generate_payment_url(response.get("Authority"))

    def create_order(self, order_obj):
        return Order.objects.create(
            user=self.request.user, shipping_address=order_obj.shipping_address
        )

    def create_order_items(self, order, order_obj):
        for item in order_obj.order_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )
