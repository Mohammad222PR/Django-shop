from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, TemplateView
from django.utils.translation import gettext_lazy as _
from cart.cart import CartSession
from cart.models import Cart
from order.forms import CheckOutOrderForm
from order.models import UserAddress, Order, OrderItem, Coupon
from order.permissions import HasCustomerAccessPermission
from payment.models import PaymentZarin, PaymentZibal
from payment.novin_pay import NovinoPay
from payment.zarinpal_client import ZarinPalSandbox
from payment.zibal_client import Zibal


# Create your views here.


class CheckOutOrderView(
    LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, FormView
):
    template_name = "order/checkout.html"
    form_class = CheckOutOrderForm
    model = Order
    success_url = reverse_lazy("order:order-completed")
    success_message = "با موفقیت ثبت شد"

    def get_form_kwargs(self):
        kwargs = super(CheckOutOrderView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data.get("address_id")
        coupon = cleaned_data.get("coupon")
        payment = self.request.POST.get("payment")
        cart = Cart.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        if payment == "zarinpal":
            return redirect(self.create_payment_zarinpal_url(order))
        if payment == "zibal":
            return redirect(self.create_payment_zibal_url(order))
        if payment == "novin":
            return redirect(self.create_payment_novin_url(order))

    def create_payment_zibal_url(self, order):
        zibal = Zibal()
        response = zibal.payment_request(order.total_price)
        payment_obj = PaymentZibal.objects.create(
            trackId=str(response.get("trackId")), amount=order.total_price
        )
        order.payment_zibal = payment_obj
        order.save()
        return zibal.generate_payment_url(response.get("trackId"))

    def create_payment_novin_url(self, order):
        novin = NovinoPay()
        response = novin.payment_request(order.total_price)
        payment_obj = PaymentZarin.objects.create(
            authority_id=response.get("authority"), amount=order.total_price
        )
        order.payment_novin = payment_obj
        order.save()
        return novin.generate_payment_url(response.get("authority"))

    def create_payment_zarinpal_url(self, order):
        zarinpal = ZarinPalSandbox()
        response = zarinpal.payment_request()
        payment_obj = PaymentZarin.objects.create(
            authority_id=response.get("Authority"), amount=order.total_price
        )
        order.payment_zarin = payment_obj
        order.save()
        return zarinpal.generate_payment_url(response.get("Authority"))

    def create_order(self, address):
        return Order.objects.create(user=self.request.user, shipping_address=address)

    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            # discount_amount = round(
            #     (total_price * Decimal(coupon.discount_percent / 100)))
            # total_price -= discount_amount

            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()
        else:
            pass

        order.total_price = total_price

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context["addresses"] = UserAddress.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 9) / 100)
        return context


class ValidateCouponView(LoginRequiredMixin, HasCustomerAccessPermission, View):

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت ثبت شد"
        total_price = 0
        total_tax = 0

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف یافت نشد"}, status=404)
        else:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "محدودیت در تعداد استفاده"

            elif coupon.expired_date and coupon.expired_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است"

            elif user in coupon.used_by.all():
                status_code, message = 403, "این کد تخفیف قبلا توسط شما استفاده شده است"

            else:
                cart = Cart.objects.get(user=self.request.user)

                total_price = cart.calculate_total_price()
                total_price = round(
                    total_price - (total_price * (coupon.discount_percent / 100))
                )
                total_tax = round((total_price * 9) / 100)
        return JsonResponse(
            {"message": message, "total_tax": total_tax, "total_price": total_price},
            status=status_code,
        )


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/order-completed.html"


class OrderFaliedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "order/order-failed.html"
