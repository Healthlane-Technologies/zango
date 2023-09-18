# Generated by Django 4.2.5 on 2023-09-21 06:04

from django.db import migrations
import zelthy.core.storage_utils


class Migration(migrations.Migration):
    dependencies = [
        ("tenancy", "0003_themesmodel_created_at_themesmodel_created_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenantmodel",
            name="fav_icon",
            field=zelthy.core.storage_utils.S3PrivateFileField(
                blank=True,
                null=True,
                upload_to=zelthy.core.storage_utils.upload_to,
                verbose_name="FavIcon",
            ),
        ),
        migrations.AlterField(
            model_name="tenantmodel",
            name="logo",
            field=zelthy.core.storage_utils.S3PrivateFileField(
                blank=True,
                null=True,
                upload_to=zelthy.core.storage_utils.upload_to,
                verbose_name="Logo",
            ),
        ),
    ]
