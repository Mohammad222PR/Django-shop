# Generated by Django 4.2.11 on 2024-05-21 21:01

import accounts.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsLetter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email address"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
            ],
            options={
                "verbose_name": "New letter",
                "verbose_name_plural": "New letters",
                "db_table": "new_letter",
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="ContactUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=40, verbose_name="Subject")),
                (
                    "first_name",
                    models.CharField(
                        default=None, max_length=20, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        default=None, max_length=20, verbose_name="last name"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        default=None,
                        max_length=13,
                        validators=[
                            accounts.validators.validate_iranian_cellphone_number
                        ],
                        verbose_name="phone number",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        default=None, max_length=40, verbose_name="email address"
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        default=None, max_length=400, verbose_name="message"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "مشاهده شده"),
                            (2, "درحال پردازش"),
                            (3, "رد شده"),
                            (4, "پاسخ داده شده"),
                            (5, "ّبسته شده"),
                        ],
                        default=2,
                        verbose_name="status",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact_us",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact us",
                "verbose_name_plural": "Contacts us",
                "db_table": "contact_us",
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="AnswerContacts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField(max_length=750, verbose_name="message")),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="created date"
                    ),
                ),
                (
                    "updated_date",
                    models.DateTimeField(auto_now=True, verbose_name="updated date"),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_contacts",
                        to="website.contactus",
                        verbose_name="Answer Contacts",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answer_contacts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
        ),
    ]
