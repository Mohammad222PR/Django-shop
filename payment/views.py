from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from order.models import Order, OrderStatus
from order.permissions import HasCustomerAccessPermission
from payment.models import PaymentZarin, PaymentStatusType, PaymentZibal
from payment.zarinpal_client import ZarinPalSandbox
from payment.zibal_client import Zibal
from shop.models import Product


class PaymentZarinVerifyView(HasCustomerAccessPermission, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("status")

        payment_obj, order = self.get_payment_and_order(authority_id)
        if not payment_obj or not order:
            return redirect(reverse_lazy("order:order-faild"))

        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(
            amount=int(payment_obj.amount), authority=authority_id
        )

        if response["Status"] in [100, 101]:
            self.handle_success_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-completed"))
        else:
            self.handle_failed_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-faild"))

    def get_payment_and_order(self, authority_id):
        payment_obj = get_object_or_404(PaymentZarin, authority_id=authority_id)
        order = get_object_or_404(Order, payment_zarin=payment_obj)
        return payment_obj, order

    def handle_success_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["RefID"]
        payment_obj.response_code = response["Status"]
        payment_obj.status = PaymentStatusType.success.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.success.value

        for item in order.order_items.all():
            product = Product.objects.get(id=item.product.id)
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.famous_percent += 1
                product.save()
            else:
                messages.error(self.request,"تعداد محصوص  میخواهید موجود نمی باشد به اندازه ای که شما ")
                return redirect(reverse_lazy("order:order-faild"))

        order.save()

    def handle_failed_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["RefID"]
        payment_obj.response_code = response["Status"]
        payment_obj.status = PaymentStatusType.failed.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.cancelled.value
        order.save()


class PaymentZibalVerifyView(HasCustomerAccessPermission, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        trackId = request.GET.get("trackId")
        status = request.GET.get("status")

        payment_obj, order = self.get_payment_and_order(trackId)
        if not payment_obj or not order:
            return redirect(reverse_lazy("order:order-faild"))

        zibal = Zibal()
        response = zibal.payment_verify(trackId=trackId)

        if response["status"] in [1, 2] or response["result"] in [100, 201]:
            self.handle_success_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-completed"))
        else:
            self.handle_failed_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-faild"))

    def get_payment_and_order(self, trackId):
        payment_obj = get_object_or_404(PaymentZibal, trackId=trackId)
        order = get_object_or_404(Order, payment_zibal=payment_obj)
        return payment_obj, order

    def handle_success_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["refNumber"]
        payment_obj.response_code = response["status"]
        payment_obj.status = PaymentStatusType.success.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.success.value
        for item in order.order_items.all():
            product = Product.objects.get(pk=item.product_id)
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.famous_percent += 1
                product.save()
            else:
                raise ValidationError(
                    f"تعداد محصوص {order.order_items.product.title} میخواهید موجود نمی باشد به اندازه ای که شما "
                )
        order.save()

    def handle_failed_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["refNumber"]
        payment_obj.response_code = response["Status"]
        payment_obj.status = PaymentStatusType.failed.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.cancelled.value
        order.save()


class PaymentNovinVerifyView(HasCustomerAccessPermission, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("authority")
        status = request.GET.get("status")

        payment_obj, order = self.get_payment_and_order(authority_id)
        if not payment_obj or not order:
            return redirect(reverse_lazy("order:order-faild"))

        zarin_pal = ZarinPalSandbox()
        response = zarin_pal.payment_verify(
            amount=int(payment_obj.amount), authority=authority_id
        )

        if response["status	"] in [100, 101]:
            self.handle_success_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-completed"))
        else:
            self.handle_failed_payment(payment_obj, order, response)
            return redirect(reverse_lazy("order:order-faild"))

    def get_payment_and_order(self, authority_id):
        payment_obj = get_object_or_404(PaymentZarin, authority_id=authority_id)
        order = get_object_or_404(Order, payment_zarin=payment_obj)
        return payment_obj, order

    def handle_success_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["ref_id"]
        payment_obj.response_code = response["status"]
        payment_obj.status = PaymentStatusType.success.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.success.value
        for item in order.order_items.all():
            product = Product.objects.get(pk=item.product_id)
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.famous_percent += 1
                product.save()
            else:
                raise ValidationError(
                    f"تعداد محصولی {order.order_items.product.title} میخواهید موجود نمی باشد به اندازه ای که شما "
                )
        order.save()

    def handle_failed_payment(self, payment_obj, order, response):
        payment_obj.ref_id = response["ref_id"]
        payment_obj.response_code = response["status"]
        payment_obj.status = PaymentStatusType.failed.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatus.cancelled.value
        order.save()
