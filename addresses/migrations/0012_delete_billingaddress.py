# Generated by Django 2.2.2 on 2019-07-25 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20190725_1509'),
        ('addresses', '0011_auto_20190725_1404'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BillingAddress',
        ),
    ]
