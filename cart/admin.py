from django.contrib import admin

from cart.models import Cart, CartItem


# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date', 'updated_date']
    list_filter = ['created_date', 'updated_date']
    search_fields = ['user']
    ordering = ['user', 'created_date', 'updated_date']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created_date', 'updated_date']
    list_filter = ['created_date', 'updated_date']
    search_fields = ['cart']
    ordering = ['cart', 'product', 'quantity', 'created_date', 'updated_date']
