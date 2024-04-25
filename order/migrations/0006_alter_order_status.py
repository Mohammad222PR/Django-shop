# Generated by Django 4.2.11 on 2024-04-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_order_total_price_default_alter_order_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "موفقیت امیز"),
                    (2, "درحال پردازش"),
                    (3, "لغو شده"),
                    (4, "ارسال شده"),
                    (5, "تحویل داده شده"),
                ],
                default=2,
                verbose_name="status",
            ),
        ),
    ]
