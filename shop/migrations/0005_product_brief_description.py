# Generated by Django 4.2.11 on 2024-03-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_remove_product_category_alter_productcategory_table_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="brief_description",
            field=models.TextField(blank=True, null=True),
        ),
    ]