from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from cart.cart import CartSession
from cart.models import Cart
from order.forms import CheckOutOrderForm
from order.models import UserAddress, Order, OrderItem
from order.permissions import HasCustomerAccessPermission


# Create your views here.


class CheckOutOrderView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutOrderForm
    model = Order
    success_url = reverse_lazy('order:order-completed')
    success_message = "با موفقیت ثبت شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context['addresses'] = UserAddress.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        total_tax = round((total_price * 9) / 100)
        context['total_price'] = total_price
        context['total_tax'] = total_tax

        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        address = cd['address_id']
        cart = Cart.objects.get(user=self.request.user)
        cart_items = cart.cart_items.all()
        order = Order.objects.get_or_create(
            user=self.request.user,
            shipping_address=address)
        for item in cart_items:
            order_item = OrderItem.objects.get_or_create(order=order, product=item.product,
                                                         price=item.product.get_price())
            order_item.quantity = item.quantity
            order_item.save()
        cart_items.delete()
        CartSession(self.request.session).clear()
        order.total_price = order.calculate_total_price()
        order.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckOutOrderView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-completed.html'
