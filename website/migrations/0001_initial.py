# Generated by Django 4.2.11 on 2024-03-24 13:31

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
                        max_length=12,
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Contact us",
                "verbose_name_plural": "Contacts us",
                "db_table": "contact_us",
                "ordering": ("created_at",),
            },
        ),
    ]
