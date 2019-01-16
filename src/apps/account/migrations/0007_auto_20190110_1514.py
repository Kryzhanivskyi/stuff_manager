# Generated by Django 2.1.4 on 2019-01-10 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20190110_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdayoffs',
            name='from_date',
            field=models.DateField(default=datetime.date.today, verbose_name='From date'),
        ),
        migrations.AlterField(
            model_name='requestdayoffs',
            name='to_date',
            field=models.DateField(default=datetime.date.today, verbose_name='To date'),
        ),
    ]
