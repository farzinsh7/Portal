from django.db import models
from account.models import User
from products.models import Product


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name='پرداخت شده / نشده')
    order_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ ثبت')

    class Meta():
        verbose_name = 'سفارش ثبت شده'
        verbose_name_plural = 'سفارش های ثبت شده'

    def __str__(self):
        return self.owner.get_full_name()


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    # price = models.IntegerField(verbose_name='قیمت محصول')
    count = models.IntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'جزییات محصولات'

    def __str__(self):
        return self.product.title
