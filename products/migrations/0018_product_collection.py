# Generated by Django 3.2.6 on 2021-10-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ManyToManyField(related_name='product', to='products.Collection', verbose_name='کالکشن'),
        ),
    ]
