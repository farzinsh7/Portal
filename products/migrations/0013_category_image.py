# Generated by Django 3.2.6 on 2021-09-04 07:25

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210831_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to=products.models.upload_image_path, verbose_name='عکس دسته بندی'),
        ),
    ]