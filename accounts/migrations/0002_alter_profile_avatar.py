# Generated by Django 4.2.11 on 2024-04-03 23:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="images/profile/customer/avatars/default/OIP.jfif",
                upload_to="images/profile/customer/avatars/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "gif", "jfif"]
                    )
                ],
                verbose_name="avatar image",
            ),
        ),
    ]
