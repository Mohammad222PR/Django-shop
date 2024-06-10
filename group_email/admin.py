from django.contrib import admin
from .models import GroupEmail
# Register your models here.

@admin.register(GroupEmail)
class GroupEmailAdmin(admin.ModelAdmin):
    list_display = ('subject',)
