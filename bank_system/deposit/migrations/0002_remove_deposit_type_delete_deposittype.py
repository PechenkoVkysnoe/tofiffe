# Generated by Django 4.2.7 on 2023-12-08 15:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("deposit", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deposit",
            name="type",
        ),
        migrations.DeleteModel(
            name="DepositType",
        ),
    ]
