from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone = models.CharField(unique=True,max_length=15, verbose_name='شماره همراه', null=True)
    is_author = models.BooleanField(default=False, verbose_name='وضعیت نویسنده')


 