# Generated by Django 4.2.11 on 2024-03-22 22:54

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True, validators=[accounts.validators.validate_iranian_cellphone_number], verbose_name='phone number'),
        ),
    ]