# Generated by Django 2.2.2 on 2019-07-24 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_auto_20190724_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='payment',
            field=models.CharField(choices=[('-', '-'), ('Наличными', 'Наличными'), ('Карточкой', 'Карточкой')], default='-', max_length=120),
        ),
    ]
