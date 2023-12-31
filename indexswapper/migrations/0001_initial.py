# Generated by Django 4.2.1 on 2023-06-17 10:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseIndex",
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
                ("code", models.CharField(max_length=6)),
                ("name", models.CharField(max_length=100)),
                (
                    "academic_units",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                ("index", models.CharField(max_length=5, unique=True)),
                ("datetime_added", models.DateTimeField(auto_now_add=True)),
                ("information", models.TextField()),
                ("pending_count", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "Course Indexes",
            },
        ),
        migrations.CreateModel(
            name="SwapRequest",
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
                ("contact_info", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("S", "Searching"),
                            ("W", "Waiting"),
                            ("C", "Completed"),
                        ],
                        default="S",
                        max_length=1,
                    ),
                ),
                ("datetime_added", models.DateTimeField(auto_now_add=True)),
                ("datetime_found", models.DateTimeField(blank=True, null=True)),
                ("wanted_indexes", models.CharField(max_length=100)),
                (
                    "current_index",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="available_swap",
                        to="indexswapper.courseindex",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="swap_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Swap Requests",
            },
        ),
    ]
