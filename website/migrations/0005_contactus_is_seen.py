# Generated by Django 4.2.11 on 2024-05-01 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_newsletter"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactus",
            name="is_seen",
            field=models.BooleanField(default=False, verbose_name="is seen"),
        ),
    ]
