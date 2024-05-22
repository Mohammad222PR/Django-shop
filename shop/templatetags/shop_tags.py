from django import template
from django.db.models import Count

from shop.models import Product, ProductStatus, WishList

register = template.Library()


@register.inclusion_tag("inc/latest-product.html", takes_context=True)
def show_latest_products(context):
    request = context.get("request", None)

    famous_products = (
        Product.objects.filter(status=ProductStatus.published.value)
        .annotate(count=Count("famous_percent"))
        .distinct()
        .order_by("-count")[:8]
    )
    wishlist_items = (
        WishList.objects.filter(user=request.user).values_list("product__id", flat=True)
        if request.user.is_authenticated
        else []
    )
    return {
        "famous_products": famous_products,
        "request": request,
        "wishlist_items": wishlist_items,
    }


@register.inclusion_tag("inc/similar-products.html", takes_context=True)
def show_similar_products(context, product):
    product_categorie = product.category.id
    request = context.get("request", None)

    similar_products = (
        Product.objects.filter(
            status=ProductStatus.published.value, category__id=product_categorie
        )
        .annotate(count=Count("famous_percent"))
        .distinct()
        .exclude(id=product.id)
        .order_by("-count")[:4]
    )
    wishlist_items = (
        WishList.objects.filter(user=request.user).values_list("product__id", flat=True)
        if request.user.is_authenticated
        else []
    )
    return {
        "similar_products": similar_products,
        "request": request,
        "wishlist_items": wishlist_items,
    }
