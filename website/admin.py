from django.contrib import admin

from website.models import ContactUs, NewsLetter


# Register your models here.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'email', 'phone_number')


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_at")
