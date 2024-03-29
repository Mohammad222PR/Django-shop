from django.contrib import admin

from website.models import ContactUs, NewsLetter


# Register your models here.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    """
    Custom admin class for the ContactUs model
    """
    list_display = ('first_name', 'last_name', 'status', 'email', 'phone_number', 'created_at')
    list_filter = ("created_at", 'status')
    ordering = ('first_name', 'last_name', 'status', 'email', 'phone_number', 'created_at')
    search_fields = ("email", 'first_name', 'last_name')


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    """
    Custom admin class for the NewsLetter model
    """
    list_display = ("id", "email", "created_at")
    list_filter = ("created_at",)
    ordering = ("created_at",)
    search_fields = ("email",)
