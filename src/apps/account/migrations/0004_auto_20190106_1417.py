# Generated by Django 2.1.4 on 2019-01-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190106_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('title', models.CharField(max_length=64)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
    ]
