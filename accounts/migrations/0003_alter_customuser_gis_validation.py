# Generated by Django 4.1.1 on 2022-12-20 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_customuser_gis_validation_customuser_items_per_grid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="gis_validation",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
