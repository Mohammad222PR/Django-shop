from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ngettext
from accounts.models import User, UserType
from shop.models import Product, ProductCategory, ProductImage
from django.contrib import messages


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'stock', 'price', 'discount_percent', 'slug', 'status', 'image_tag',
                    'created_date', 'updated_date', 'famous_percent']
    list_filter = ['status', 'created_date', 'updated_date', 'famous_percent']
    inlines = [ProductImageAdmin]
    search_fields = ['title']
    ordering = ['user', 'title', 'stock', 'price', 'discount_percent', 'slug', 'status', 'image',
                'created_date', 'updated_date']
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(Q(type=2) | Q(type=3))
        return super(ProductAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_date']
    list_filter = ['created_date']
    search_fields = ['title', 'slug', ]
    ordering = ['title', 'slug', 'created_date']
    prepopulated_fields = {'slug': ('title',)}
