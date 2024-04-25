from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from shop.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg


# Create your models here.
class ReviewStatus(models.IntegerChoices):
    pending = 1, _("درانتظار تایید")
    accepted = 2, _("تایید شده")
    rejected = 3, _("رد شده")


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("user")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("product"),
    )
    description = models.CharField(max_length=400, verbose_name=_("description"))
    rate = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(5, message=_("Max value is 5")),
            MinValueValidator(0, message=_("Min value is 0")),
        ],
    )
    status = models.IntegerField(
        choices=ReviewStatus.choices,
        default=ReviewStatus.pending.value,
        verbose_name=_("status"),
    )

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        db_table = "reviews"
        ordering = ('created_date',)

    def get_status(self):
        return {
            "id":self.status,
            "title": ReviewStatus(self.status).name,
            "label": ReviewStatus(self.status).label,
        }
    def __str__(self):
        return f"{self.user.user_profile.full_name} ==> {self.product.title}"


@receiver(post_save, sender=Review)
def calculate_avg_review(sender, instance, created, **kwargs):
    if instance.status == ReviewStatus.accepted.value:
        product = instance.product
        average_rating = Review.objects.filter(
            product=product, status=ReviewStatus.accepted
        ).aggregate(Avg("rate"))["rate__avg"]
        product.avg_rate = round(average_rating, 1)
        product.save()
