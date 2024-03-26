from django.shortcuts import render, get_object_or_404
from django.views import generic
from faker.utils.text import slugify

from shop.models import Product, ProductStatus

# Create your views here.
status = ProductStatus


class ProductGridView(generic.ListView):
    template_name = 'shop/product-grid.html'
    model = Product
    queryset = Product.objects.filter(status=status.published.value)
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'shop/product-detail.html'
    context_object_name = 'product'

