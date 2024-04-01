from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerProfile
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """

    list_display = ("id", "email", "is_superuser", "is_active", "type", "is_verified")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    searching_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions", "type"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )


@admin.register(CustomerProfile)
class CustomProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "image_tag",
        "last_name",
        "phone_number",
    )
    searching_fields = ("user", "first_name", "last_name", "phone_number")
    list_filter = ("id", "user", "first_name", "last_name", "phone_number")
    ordering = ("id",)
