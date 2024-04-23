from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from shop.models import Product


# Create your models here.


class Cart(models.Model):
    """
    Cart model for user cart
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts", verbose_name=_("user")
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ("-created_date",)
        db_table = "cart"

    def __str__(self):
        return self.user.email

    def calculate_total_price(self):
        return sum(
            item.product.get_price() * item.quantity for item in self.cart_items.all()
        )


class CartItem(models.Model):
    """
    CartItem model for product cart items related to cart user
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("cart"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
        verbose_name=_("product"),
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")
        ordering = ("-created_date",)
        db_table = "cart_items"

    def __str__(self):
        return self.product.title
