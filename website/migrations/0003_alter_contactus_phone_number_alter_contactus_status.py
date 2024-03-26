# Generated by Django 4.2.11 on 2024-03-25 10:58

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_contactus_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='phone_number',
            field=models.CharField(default=None, max_length=13, validators=[accounts.validators.validate_iranian_cellphone_number], verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='status',
            field=models.IntegerField(choices=[(1, 'مشاهده شده'), (2, 'درحال پردازش'), (3, 'رد شده')], default=2, verbose_name='status'),
        ),
    ]
