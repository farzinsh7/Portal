# Generated by Django 3.2.6 on 2021-08-30 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='parts',
            field=models.IntegerField(default=1, verbose_name='تعداد قطعات مونتاژ'),
        ),
    ]
