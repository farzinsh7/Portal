# Generated by Django 3.2.6 on 2021-08-30 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210830_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='products/% Y/% m/% d/', verbose_name='عکس محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='products/% Y/% m/% d/', verbose_name='ادیت محصول'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_3d',
            field=models.FileField(null=True, upload_to='model-3d/% Y/% m/% d/', verbose_name='فایل سه بعدی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model_3d_1',
            field=models.FileField(blank=True, null=True, upload_to='model-3d/% Y/% m/% d/', verbose_name='فایل سه بعدی'),
        ),
    ]