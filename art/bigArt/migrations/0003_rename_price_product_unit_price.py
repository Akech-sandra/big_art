# Generated by Django 5.0.6 on 2024-07-12 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bigArt", "0002_product_artist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="unit_price",
        ),
    ]
