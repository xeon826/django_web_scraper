# Generated by Django 4.1.1 on 2022-12-20 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0005_settings_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="settings",
            name="gis_validation",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
