from django.contrib import admin

from payment.models import PaymentZarin, PaymentZibal


# Register your models here.


@admin.register(PaymentZarin)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "authority_id",
        "ref_id",
        "amount",
        "response_json",
        "response_code",
        "status",
        "created_date",
        "updated_date",
    ]
    list_filter = [
        "status",
        "created_date",
        "updated_date",
    ]


@admin.register(PaymentZibal)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "trackId",
        "ref_id",
        "amount",
        "response_json",
        "response_code",
        "status",
        "created_date",
        "updated_date",
    ]
    list_filter = [
        "status",
        "created_date",
        "updated_date",
    ]


