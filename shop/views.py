from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import ValidationError, FieldError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from faker.utils.text import slugify
from typing import Any

from accounts.models import UserType
from cart.cart import CartSession
from review.models import ReviewStatus, Review
from shop.models import Product, ProductStatus, ProductCategory, WishList

# Create your views here.
status = ProductStatus


class ProductGridView(generic.ListView):
    template_name = "shop/product-grid.html"
    context_object_name = "products"
    paginate_by = 7

    def get_paginate_by(self, queryset):
        return self.request.GET.get("page_size", self.paginate_by)

    def get_queryset(self):
        queryset = Product.objects.filter(status=status.published.value).distinct()
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
        context["wishlist_items"] = (
            WishList.objects.filter(user=self.request.user).values_list(
                "product__id", flat=True
            )
            if self.request.user.is_authenticated
            else []
        )
        context["categories"] = ProductCategory.objects.all().distinct()
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "shop/product-detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["is_wished"] = (
            WishList.objects.filter(
                user=self.request.user, product__id=product.id
            ).exists()
            if self.request.user.is_authenticated
            else False
        )
        reviews = Review.objects.filter(product=product,status=ReviewStatus.accepted.value)
        context["reviews"] = reviews
        total_reviews_count =reviews.count()
        reviews_count = {
            f"rate_{rate}": reviews.filter(rate=rate).count() for rate in range(1, 6)
        }
        if total_reviews_count != 0:
            reviews_avg = {
                f"rate_{rate}": round((reviews.filter(rate=rate).count()/total_reviews_count)*100,2) for rate in range(1, 6)
            }
        else:
            reviews_avg = {f"rate_{rate}": 0 for rate in range(1, 6)}

        customer_recommend = round(reviews.filter(rate__in=[4, 5]).count() * total_reviews_count / 2)
        context["reviews_count"]  = reviews_count
        context["reviews_avg"] = reviews_avg
        context["reviews_avg"] = reviews_avg
        context['customer_recommend'] = customer_recommend
        return context
        # another method
        """
        reviews = Review.objects.filter(product=product, status=ReviewStatus.accepted.value)

        total_reviews_count = reviews.count()

        reviews_count = reviews.values('rate').annotate(count=Count('rate'))

        reviews_avg = {
            f"{rate['rate']}": round((rate['count'] / total_reviews_count) * 100, 2)
            for rate in reviews_count
        }

        customer_recommend = round((reviews.filter(rate=5).count()) * total_reviews_count / 2)

        context["reviews"] = reviews
        context["reviews_count"] = {f"{rate['rate']}": rate['count'] for rate in reviews_count}
        context["reviews_avg"] = reviews_avg
        context['customer_recommend'] = customer_recommend
        """

class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id and UserType.superuser.value or UserType.customer.value:
            try:
                wishlist_item = WishList.objects.get(
                    user=request.user, product__id=product_id
                )
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishList.DoesNotExist:
                WishList.objects.create(user=request.user, product_id=product_id)
                message = "محصول به لیست علایق اضافه شد"

        return JsonResponse({"message": message})

