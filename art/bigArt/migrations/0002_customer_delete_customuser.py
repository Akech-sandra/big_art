# Generated by Django 5.0.6 on 2024-06-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bigArt", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100)),
                ("phone", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                ("gender", models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
