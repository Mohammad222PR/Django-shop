import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User
from django.utils.translation import gettext_lazy as _

from payment.models import PaymentZarin, PaymentZibal, PaymentNovin
from shop.models import Product


class OrderStatus(models.IntegerChoices):
    success = 1, _("موفقیت امیز")
    pending = 2, _("درحال پردازش")
    cancelled = 3, _("لغو شده")
    posted = 4, _("ارسال شده")
    delivered = 5, _("تحویل داده شده")


# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("discount percent"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    max_limit_usage = models.PositiveIntegerField(
        default=10, verbose_name=_("max limit usage")
    )
    used_by = models.ManyToManyField(
        User,
        verbose_name=_("used by"),
        related_name="coupon_user",
        null=True,
        blank=True,
    )
    expired_date = models.DateTimeField(verbose_name=_("expired date"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    def __str__(self):
        return self.code


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
    shipping_address = models.ForeignKey(
        UserAddress,
        on_delete=models.PROTECT,
        related_name="shipping_address",
        verbose_name=_("shipping"),
    )
    payment_zarin = models.ForeignKey(
        PaymentZarin,
        on_delete=models.SET_NULL,
        verbose_name="payment zarin",
        null=True,
        blank=True,
    )
    payment_zibal = models.ForeignKey(
        PaymentZibal,
        on_delete=models.SET_NULL,
        verbose_name="payment zibal",
        null=True,
        blank=True,
    )
    payment_novin = models.ForeignKey(
        PaymentNovin,
        on_delete=models.SET_NULL,
        verbose_name="payment novin",
        null=True,
        blank=True,
    )

    total_price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("total price")
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



    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    def get_status(self):
        return {
            "id": self.status,
            "title": OrderStatus(self.status).name,
            "label": OrderStatus(self.status).label,
        }

    def get_price(self):
        if self.coupon:
            discounted_price = round(
                self.total_price
                - (self.total_price * Decimal(self.coupon.discount_percent / 100))
            )
            return discounted_price
        else:
            return self.total_price

    @property
    def is_successful(self):
        return self.status == OrderStatus.success.value


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
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
