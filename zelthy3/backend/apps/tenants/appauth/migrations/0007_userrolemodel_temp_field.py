# Generated by Django 4.2.2 on 2023-08-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appauth', '0006_alter_userrolemodel_policies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrolemodel',
            name='temp_field',
            field=models.CharField(max_length=20, null=True),
        ),
    ]