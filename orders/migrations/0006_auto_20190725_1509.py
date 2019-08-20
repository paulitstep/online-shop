# Generated by Django 2.2.2 on 2019-07-25 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190725_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='addresses.Address'),
        ),
    ]
