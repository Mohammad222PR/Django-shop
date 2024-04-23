from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class PaymentStatusType(models.IntegerChoices):
    pending = 1, _("در انتظار")
    success = 2, _("پرداخت موفق")
    failed = 3, _("پرداخت ناموفق")


class PaymentZarin(models.Model):
    authority_id = models.CharField(max_length=255, verbose_name=_("Authority"))
    ref_id = models.BigIntegerField(verbose_name=_("ref id"), null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("amount")
    )
    response_json = models.JSONField(default=dict, verbose_name=_("response json"))
    response_code = models.IntegerField(
        null=True, blank=True, verbose_name=_("response code")
    )
    status = models.IntegerField(
        choices=PaymentStatusType.choices,
        default=PaymentStatusType.pending.value,
        verbose_name=_("status"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    def __str__(self):
        return self.authority_id


class PaymentZibal(models.Model):
    trackId = models.CharField(max_length=255, verbose_name=_("trackId"))
    ref_id = models.BigIntegerField(verbose_name=_("ref id"), null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("amount")
    )
    response_json = models.JSONField(default=dict, verbose_name=_("response json"))
    response_code = models.IntegerField(
        null=True, blank=True, verbose_name=_("response code")
    )
    status = models.IntegerField(
        choices=PaymentStatusType.choices,
        default=PaymentStatusType.pending.value,
        verbose_name=_("status"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    def __str__(self):
        return self.trackId


class PaymentNovin(models.Model):
    authority_id = models.CharField(max_length=255, verbose_name=_("Authority"))
    ref_id = models.BigIntegerField(verbose_name=_("ref id"), null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("amount")
    )
    response_json = models.JSONField(default=dict, verbose_name=_("response json"))
    response_code = models.IntegerField(
        null=True, blank=True, verbose_name=_("response code")
    )
    status = models.IntegerField(
        choices=PaymentStatusType.choices,
        default=PaymentStatusType.pending.value,
        verbose_name=_("status"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    def __str__(self):
        return self.authority_id
