from typing import Any
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, TemplateView, UpdateView

from cart.cart import CartSession
from shop.models import Product, ProductStatus


class SessionAddProduct(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        if product_id:
            cart.add_product(product_id, quantity)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionCartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context


class SessionUpdateProductQuantityView(View):
    template_name = 'cart/cart-summary.html'

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        if product_id and quantity:
            cart.update_product_quantity(product_id, quantity)
            messages.success(request, "تعداد محصول با موفقیت به‌روزرسانی شد", 'success')
        else:
            messages.error(request, "خطا در به‌روزرسانی تعداد محصول", 'danger')
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})



class SessionRemoveProductView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get('product_id')
        if product_id:
            cart.remove_product(product_id)
            messages.success(request, "محصول با موفقیت حذف شد", 'success')
        else:
            messages.error(request, "خطا در حذف محصول", 'danger')

        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})
