from django.contrib import admin

from website.models import ContactUs


# Register your models here.
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status' ,'email', 'phone_number')




