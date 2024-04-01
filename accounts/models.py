from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator

from accounts.validators import validate_iranian_cellphone_number


# from accounts.validators import validate_iranian_cellphone_number


class UserType(models.IntegerChoices):
    customer = 1, _("customer")
    admin = 2, _("admin")
    superuser = 3, _("superuser")


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.superuser.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    is_staff = models.BooleanField(default=False, verbose_name=_("staff status"))
    is_active = models.BooleanField(default=True, verbose_name=_("active status"))
    is_verified = models.BooleanField(default=False, verbose_name=_("verified status"))
    type = models.IntegerField(
        choices=UserType.choices,
        default=UserType.customer.value,
        verbose_name=_("type user"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created date")
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name=_("updated date"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="user_profile",
    )
    phone_number = models.CharField(
        max_length=12,
        validators=[validate_iranian_cellphone_number],
        verbose_name=_("phone number"),
        unique=True,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=30, verbose_name=_("first name"), default=""
    )
    last_name = models.CharField(max_length=30, verbose_name=_("last name"), default="")
    avatar = models.ImageField(
        upload_to="images/profile/customer/avatars/",
        blank=True,
        default="images/profile/customer/avatars/default/OIP.jfif",
        verbose_name=_("avatar image"),
    )

    def image_tag(self):
        return format_html(
            "<img src='{}' width=100 height=100 style='border-radius: 10px;'>".format(
                self.avatar.url
            )
        )

    image_tag.short_description = _("avatar")

    def full_name(self):
        return self.first_name + " " + self.last_name

    full_name.short_description = _("full name")


@receiver(post_save, sender=User)
def create_user_customer_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.customer.value:
        CustomerProfile.objects.create(user=instance, pk=instance.pk)
