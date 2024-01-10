# Generated by Django 4.2.5 on 2023-10-18 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.CharField(blank=True, editable=False, max_length=255),
                ),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "modified_by",
                    models.CharField(blank=True, editable=False, max_length=255),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("is_enabled", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
                ("args", models.JSONField(blank=True, null=True)),
                ("kwargs", models.JSONField(blank=True, null=True)),
                (
                    "attached_policies",
                    models.ManyToManyField(
                        blank=True, null=True, to="permissions.policymodel"
                    ),
                ),
                (
                    "crontab",
                    models.ForeignKey(
                        blank=True,
                        help_text="Crontab Schedule",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.crontabschedule",
                        verbose_name="crontab",
                    ),
                ),
                (
                    "interval",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.intervalschedule",
                        verbose_name="interval",
                    ),
                ),
                (
                    "master_task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_celery_beat.periodictask",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
