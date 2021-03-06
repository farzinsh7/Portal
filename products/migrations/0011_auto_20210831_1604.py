# Generated by Django 3.2.6 on 2021-08-31 11:34

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210831_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='model_3dm',
            field=models.FileField(null=True, upload_to=products.models.upload_image_path, verbose_name='فایل سه بعدی (3DM)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_stl',
            field=models.FileField(null=True, upload_to=products.models.upload_image_path, verbose_name='فایل سه بعدی (STL)'),
        ),
    ]
