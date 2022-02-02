import os

from django.utils.html import format_html

from extensions.utils import jalali_converter
from account.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.publish}-{instance.title}{ext}"
    return f"products/{final_name}"


class ProductsManager(models.Manager):

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


class Category(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(verbose_name='آدرس دسته‌بندی', max_length=300, unique=True)
    image = models.ImageField(upload_to='category', null=True, verbose_name='عکس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی ها'

    def get_absolute_url(self):
        return reverse('account:category')


class Collection(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان کالکشن')
    slug = models.SlugField(verbose_name='شناسه کالکشن', max_length=300, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کالکشن'
        verbose_name_plural = 'کالکشن ها'

    def get_absolute_url(self):
        return reverse('account:collection')


class Product(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),
        ('p', 'انتشار')
    )
    title = models.CharField(max_length=300, verbose_name='عنوان محصول')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='نویسنده')
    parts = models.IntegerField(default=1, verbose_name='تعداد قطعات مونتاژ')
    slug = models.SlugField(verbose_name='آدرس محصول', null=True, max_length=200, unique=True)
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name='product')
    collection = models.ManyToManyField(Collection, verbose_name='کالکشن', related_name='product')
    description = models.TextField(verbose_name='توضیحات بیشتر', null=True, blank=True)
    color = models.CharField(max_length=300, verbose_name='رنگ', null=True, blank=True)
    technique = models.CharField(max_length=300, verbose_name='تکنیک', null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='عکس محصول')
    image_1 = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='ادیت محصول')
    model_3dm = models.FileField(upload_to=upload_image_path, null=True, blank=True, verbose_name='فایل سه بعدی (3DM)')
    model_3dm_1 = models.FileField(upload_to=upload_image_path, null=True, blank=True,
                                   verbose_name='ادیت فایل سه بعدی (3DM)')
    model_stl = models.FileField(upload_to=upload_image_path, null=True, blank=True, verbose_name='فایل سه بعدی (STL)')
    model_stl_1 = models.FileField(upload_to=upload_image_path, null=True, blank=True,
                                   verbose_name='ادیت فایل سه بعدی (STL)')
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, verbose_name='وضعیت')

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):
        return reverse('account:dashboard')

    def get_absolute(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}"

    def category_to_str(self):
        return ",".join([category.title for category in self.category_published()])

    category_to_str.short_description = 'دسته‌بندی'

    def collection_to_str(self):
        return ",".join([collection.slug for collection in self.collection_all()])

    collection_to_str.short_description = 'کالکشن'

    def collection_all(self):
        return self.collection.all()

    def category_published(self):
        return self.category.filter(status=True)

    def j_publish(self):
        return jalali_converter(self.publish)

    j_publish.short_description = 'زمان انتشار'

    objects = ArticleManager()

