# Generated by Django 3.2.6 on 2021-08-31 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_author',
            field=models.BooleanField(default=False, verbose_name='وضعیت نویسنده'),
        ),
    ]
