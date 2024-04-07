from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User
from django.utils.translation import gettext_lazy as _

from shop.models import Product


class OrderStatus(models.IntegerChoices):
    processing = 1, _("درحال پردازش")
    pending = 2, _("درانتظار پرداخت")
    shipping = 3, _("ارسال شده")
    delivered = 4, _("تحویل شده")
    cancelled = 5, _("لغو شده")


# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=100)
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("discount percent"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    max_limit_usage = models.PositiveIntegerField(
        default=10, verbose_name=_("max limit usage")
    )
    used_by = models.ManyToManyField(
        User, verbose_name=_("used by"), related_name="coupon_user", null=True, blank=True
    )
    expired_date = models.DateTimeField(verbose_name=_("expired date"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))


class Meta:
    verbose_name = _("Coupon")
    verbose_name_plural = _("Coupons")
    ordering = ("created_date", "updated_date")
    db_table = "coupon"


class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("user")
    )
    address = models.CharField(max_length=250, verbose_name=_("address"))
    state = models.CharField(max_length=50, verbose_name=_("state"))
    city = models.CharField(max_length=50, verbose_name=_("city"))
    zip_code = models.CharField(max_length=50, verbose_name=_("zip code"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))
    class Meta:
        verbose_name = _("User address")
        verbose_name_plural = _("User addresses")
        ordering = ("created_date", "updated_date")
        db_table = "user_address"

    def __str__(self):
        return self.address


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="orders", verbose_name=_("user")
    )

    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.pending.value,
        verbose_name=_("status"),
    )
    shipping_address = models.OneToOneField(
        UserAddress,
        on_delete=models.PROTECT,
        related_name="shipping_address",
        verbose_name=_("shipping"),
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("total_price")
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.PROTECT,
        verbose_name=_("coupon"),
        null=True,
        blank=True,
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("created_date", "updated_date")
        db_table = "order"

    def __str__(self):
        return self.user.user_profile.full_name()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_item",
        verbose_name=_("order"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("product"),
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("price")
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")
        ordering = ("-created_date",)
        db_table = "order_items"

    def __str__(self):
        return self.product.title
