# Generated by Django 4.1 on 2022-09-14 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="manufacturer",
            name="manufacturer",
        ),
    ]
