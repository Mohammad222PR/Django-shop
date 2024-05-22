from django.contrib import sitemaps
from .models import Product, ProductStatus
from django.urls import reverse


class ProductSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(status=ProductStatus.published.value)

    def lastmod(self, obj):
        return obj.updated_date
    
    def location(self,item):
        return reverse('shop:product-detail',kwargs={'slug':item.slug})
    
