# Generated by Django 2.2.2 on 2019-07-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0008_auto_20190724_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(default='shipping', max_length=120),
        ),
    ]
