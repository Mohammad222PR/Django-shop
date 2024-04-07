from django.contrib import admin

from order.models import Coupon, UserAddress, Order, OrderItem


# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "discount_percent",
        "max_limit_usage",
        "used_by_count",
        "expired_date",
        "created_date",
        "updated_date",
    ]
    list_filter = ["expired_date", "created_date", "updated_date", ]

    search_fields = ["code", ]
    ordering = [
        "code",
        "discount_percent",
        "max_limit_usage",
        "used_by",
        "expired_date",
        "created_date",
        "updated_date",
    ]

    def used_by_count(self, obj):
        return obj.used_by.count()


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["user", "address", "state", "city", "zip_code", "created_date",
                    "updated_date", ]
    list_filter = ["state", "city", ]

    search_fields = ["state", "city", ]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
        "shipping_address",
        "total_price",
        "coupon",
        "created_date",
        "updated_date",
    ]
    list_filter = ["created_date", "updated_date", "status", ]
    search_fields = ["user", ]
    ordering = [
        "user",
        "status",
        "shipping_address",
        "total_price",
        "coupon",
        "created_date",
        "updated_date",
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "product",
        "price",
        "quantity",
        "created_date",
        "updated_date",
    ]
    list_filter = ["created_date", "updated_date", ]
    search_fields = ["order", "product", ]
    ordering = ["order", "product", "price", "quantity", "created_date", "updated_date", ]
