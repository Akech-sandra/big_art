# Generated by Django 5.0.6 on 2024-06-14 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bigArt", "0002_customer_delete_customuser"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Customer",
            new_name="CustomUser",
        ),
    ]