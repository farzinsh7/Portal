# Generated by Django 3.2.6 on 2021-08-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210830_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='parts',
            field=models.IntegerField(default=1),
        ),
    ]
