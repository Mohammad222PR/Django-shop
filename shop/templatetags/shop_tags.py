from django import template
from django.db.models import Count

from shop.models import Product, ProductStatus

register = template.Library()


@register.inclusion_tag('inc/latest-product.html')
def show_latest_products():
    famous_products = Product.objects.filter(status=ProductStatus.published.value).annotate(
        count=Count('famous_percent')).order_by('-count')[:8]
    return {'famous_products': famous_products}


@register.inclusion_tag('inc/similar-products.html')
def show_similar_products(product):
    product_categories = product.category.all()
    similar_products = Product.objects.filter(status=ProductStatus.published.value, category__in=product_categories).order_by('-created_date')[:4]

    return {'similar_products': similar_products}
