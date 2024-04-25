from django.contrib import admin

from review.models import Review


# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "description",
        "rate",
        "status",
        "created_date",
        "updated_date",
    ]
