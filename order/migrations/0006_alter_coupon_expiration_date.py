# Generated by Django 4.2.11 on 2024-04-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_alter_order_shipping_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="expired_date",
            field=models.DateTimeField(verbose_name="expiration date"),
        ),
    ]
