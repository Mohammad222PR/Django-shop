from django.contrib import admin
from django.contrib.sessions.models import Session
from cart.models import Cart, CartItem


# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "created_date", "updated_date"]
    list_filter = ["created_date", "updated_date"]
    search_fields = ["user"]
    ordering = ["user", "created_date", "updated_date"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity", "created_date", "updated_date"]
    list_filter = ["created_date", "updated_date"]
    search_fields = ["cart"]
    ordering = ["cart", "product", "quantity", "created_date", "updated_date"]


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]


admin.site.register(Session, SessionAdmin)
