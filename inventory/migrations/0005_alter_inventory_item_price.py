# Generated by Django 4.1 on 2022-08-22 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0004_cartitem_total_alter_cartitem_product_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="item_price",
            field=models.FloatField(default=0),
        ),
    ]