# Generated by Django 4.1.2 on 2022-11-29 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ESite_App", "0005_alter_shippingaddress_address_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BackgroundImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Background_Image", models.ImageField(upload_to="")),
            ],
        ),
    ]