# Generated by Django 4.2.4 on 2023-08-30 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_models', '0010_delete_abstractpatient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
