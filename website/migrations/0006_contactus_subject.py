# Generated by Django 4.2.11 on 2024-05-01 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_contactus_is_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactus",
            name="subject",
            field=models.CharField(default=1, max_length=40, verbose_name="Subject"),
            preserve_default=False,
        ),
    ]