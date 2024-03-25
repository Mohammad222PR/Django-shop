from django.core.validators import RegexValidator
from django.db import models

from accounts.validators import validate_iranian_cellphone_number
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Status(models.IntegerChoices):
    success = 1, _('مشاهده شده')
    pending = 2, _('درحال پردازش')
    ignored = 3, _('رد شده')


class ContactUs(models.Model):
    first_name = models.CharField(max_length=20, default=None, verbose_name=_('first name'))
    last_name = models.CharField(max_length=20, default=None, verbose_name=_('last name'))
    phone_number = models.CharField(max_length=13, validators=[validate_iranian_cellphone_number], default=None,
                                    verbose_name=_('phone number'))
    email = models.EmailField(max_length=40, default=None, verbose_name=_('email address'))
    message = models.TextField(max_length=400, default=None, verbose_name=_('message'))
    status = models.IntegerField(choices=Status.choices, default=Status.pending.value, verbose_name=_('status'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contacts us'
        db_table = 'contact_us'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
