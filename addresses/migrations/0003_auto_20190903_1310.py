# Generated by Django 2.2.2 on 2019-09-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190903_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
