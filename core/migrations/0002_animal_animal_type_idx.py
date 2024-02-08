# Generated by Django 4.1.5 on 2024-02-08 13:37

import django.core.validators
from django.db import migrations, models

import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Animal",
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
                ("name", models.CharField(max_length=20)),
                (
                    "age",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(360),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("dog", "DOG"), ("cat", "CAT")], max_length=10
                    ),
                ),
                ("entry_date", models.DateField()),
                ("decsription", models.CharField(max_length=120)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("large", "LARGE"),
                            ("medium", "MEDIUM"),
                            ("small", "SMALL"),
                        ],
                        default=core.utils.AnimalSize["MEDIUM"],
                        max_length=6,
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "AVALIABLE"), (1, "RESERVED"), (3, "ADOPTED")],
                        default=core.utils.AnimalStatus["AVALIABLE"],
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("male", "MALE"), ("female", "FEMALE")], max_length=6
                    ),
                ),
                ("requirements", models.CharField(max_length=100)),
                ("img_link", models.CharField(blank=True, max_length=200)),
            ],
            options={
                "ordering": ["entry_date"],
            },
        ),
        migrations.AddIndex(
            model_name="animal",
            index=models.Index(fields=["type"], name="type_idx"),
        ),
    ]
