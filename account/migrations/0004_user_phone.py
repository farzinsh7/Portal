# Generated by Django 5.1.2 on 2024-11-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='شماره همراه'),
        ),
    ]