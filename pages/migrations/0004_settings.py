# Generated by Django 4.1.1 on 2022-12-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_item_assigned_to"),
    ]

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gis_validation", models.BooleanField()),
            ],
        ),
    ]
