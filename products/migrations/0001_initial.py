# Generated by Django 3.2.6 on 2021-08-30 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان دسته\u200cبندی')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='آدرس دسته\u200cبندی')),
                ('status', models.BooleanField(default=True, verbose_name='آیا نمایش داده شود')),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان محصول')),
                ('slug', models.SlugField(max_length=200, null=True, unique=True, verbose_name='آدرس محصول')),
                ('description', models.TextField(null=True, verbose_name='توضیحات بیشتر')),
                ('image', models.ImageField(null=True, upload_to='product-image', verbose_name='عکس محصول')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='product-image', verbose_name='ادیت محصول')),
                ('model_3d', models.FileField(null=True, upload_to='product-3d', verbose_name='فایل سه بعدی')),
                ('model_3d_1', models.FileField(blank=True, null=True, upload_to='product-3d', verbose_name='فایل سه بعدی')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('status', models.CharField(choices=[('d', 'پیش\u200cنویس'), ('p', 'انتشار')], max_length=1, null=True, verbose_name='وضعیت')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('category', models.ManyToManyField(to='products.Category', verbose_name='دسته\u200cبندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
    ]
