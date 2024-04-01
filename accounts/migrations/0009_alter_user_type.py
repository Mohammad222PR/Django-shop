# Generated by Django 4.2.11 on 2024-04-01 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_customerprofile_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="type",
            field=models.IntegerField(
                choices=[
                    (1, "customer"),
                    (2, "admin"),
                    (3, "superuser"),
                    (4, "support"),
                ],
                default=1,
                verbose_name="type user",
            ),
        ),
    ]
