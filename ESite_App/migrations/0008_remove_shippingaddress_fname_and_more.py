# Generated by Django 4.1.2 on 2022-12-05 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ESite_App", "0007_remove_item_categories_item_category"),
    ]

    operations = [
        migrations.RemoveField(model_name="shippingaddress", name="fname",),
        migrations.RemoveField(model_name="shippingaddress", name="lname",),
        migrations.AlterField(
            model_name="shippingaddress",
            name="address",
            field=models.TextField(default=None, max_length=400),
        ),
    ]