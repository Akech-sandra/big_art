# Generated by Django 5.0.6 on 2024-07-01 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bigArt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="painting",
            name="price",
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="painting",
            name="short_description",
            field=models.TextField(default="No description available"),
        ),
        migrations.AlterField(
            model_name="painting",
            name="artist",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="painting",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
