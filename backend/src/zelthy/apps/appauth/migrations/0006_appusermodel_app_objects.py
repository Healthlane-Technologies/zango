# Generated by Django 4.2.8 on 2024-01-10 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appauth", "0005_remove_appusermodel_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="appusermodel",
            name="app_objects",
            field=models.JSONField(null=True),
        ),
    ]
