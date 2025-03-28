# Generated by Django 5.1.6 on 2025-03-16 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RegKey",
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
                ("reg_key", models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("user_tag", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=8)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "reg_key",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="tasks.regkey"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("completed", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user_tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tasks.user"
                    ),
                ),
            ],
        ),
    ]
