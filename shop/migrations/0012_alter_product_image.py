# Generated by Django 4.2.11 on 2024-04-04 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0011_alter_productimage_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="images/products/default_img/product-default.png",
                upload_to="images/products",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["jpg", "jpeg", "png", "jfif"],
                        message="اپلود تصویر با پسوند“%(extension)s” مجاز نیست پسوند های مجاز jpg, png, jfif, jpeg",
                    )
                ],
                verbose_name="image",
            ),
        ),
    ]
