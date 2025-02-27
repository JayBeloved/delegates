# Generated by Django 5.1.6 on 2025-02-07 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delegate",
            name="status",
            field=models.CharField(
                choices=[("Unassigned", "Unassigned"), ("Assigned", "Assigned")],
                default="Unassigned",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Payment",
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
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("Bank Transfer", "Bank Transfer"),
                            ("Portal", "Portal"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "amount",
                    models.CharField(
                        choices=[
                            ("Full", "Full"),
                            ("30000", "30,000"),
                            ("60000", "60,000"),
                        ],
                        max_length=6,
                    ),
                ),
                ("verified", models.BooleanField(default=False)),
                (
                    "delegate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.delegate"
                    ),
                ),
            ],
        ),
    ]
