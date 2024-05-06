from decimal import Decimal

from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import User


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=40, verbose_name=_("title"), default=None)
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name=_("slug"),
        default=None,
        allow_unicode=True,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="product_categories",
        verbose_name="parent",
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )

    class Meta:
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")
        ordering = ("created_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(ProductCategory, self).save(*args, **kwargs)


class ProductStatus(models.IntegerChoices):
    published = 1, _("نمایش")
    draft = 2, _("عدم نمایش ")


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("user"))
    title = models.CharField(max_length=40, verbose_name=_("title"), default=None)
    description = CKEditor5Field(verbose_name=_("description"))
    brief_description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, verbose_name=_("stock"))
    price = models.DecimalField(
        max_digits=10, decimal_places=0, default=0, verbose_name=_("price")
    )
    discount_percent = models.IntegerField(
        default=0,
        verbose_name=_("discount percent"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name=_("slug"),
        default=None,
        allow_unicode=True,
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name=_("category"),
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.IntegerField(
        choices=ProductStatus.choices,
        default=ProductStatus.draft.value,
        verbose_name=_("status"),
    )
    famous_percent = models.IntegerField(
        default=0, verbose_name=_("famous percent"), blank=True, null=True
    )
    avg_rate = models.FloatField(default=0, verbose_name=_("avg rate"))
    image = models.ImageField(
        upload_to="images/products",
        verbose_name=_("image"),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "jfif"],
                message="اپلود تصویر با پسوند“%(extension)s” مجاز نیست پسوند های مجاز jpg, png, jfif, jpeg",
            )
        ],
        default="images/products/default_img/product-default.png",
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ("created_date", "updated_date")
        db_table = "product"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)

    # def new_product(self):
    #     date = datetime.today() + timedelta(days=7)
    #     if self.created_date.date() != datetime.today(date):
    #         return True
    #     else:
    #         return False

    def get_price(self):
        if self.discount_percent > 0:
            discount_amount = self.price * Decimal(self.discount_percent / 100)
            discounted_amount = self.price - discount_amount
            return round(discounted_amount)

    def image_tag(self):
        return format_html(
            "<img src='{}' width=100 height=100 style='border-radius: 10px;'>".format(
                self.image.url
            )
        )

    image_tag.short_description = _("image")

    def is_published(self):
        return self.status == ProductStatus.published.value

    def is_discount(self):
        return self.discount_percent != 0

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("product"),
        related_name="product_image",
    )
    file = models.ImageField(
        upload_to="images/products/many_image/",
        default="images/products/default_img/product-default.png",
        verbose_name=_("file"),
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        db_table = "product_image"
        ordering = ("created_date", "updated_date")

    def __str__(self):
        return str(self.product.title)


class WishList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wish_list", verbose_name=_("user")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wish_list",
        verbose_name=_("product"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        verbose_name = _("WishList")
        verbose_name_plural = _("WishLists")
        db_table = "wish_list"
        ordering = ("created_date", "updated_date")

    def __str__(self):
        return f"{self.product.title} - {self.user.user_profile.full_name()}"
