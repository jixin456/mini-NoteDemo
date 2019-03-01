# Generated by Django 2.1 on 2019-02-27 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190227_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_idv',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_id',
            field=models.CharField(default='af772fde2b724341ad632e2bf3a7c2b9', max_length=50, unique=True, verbose_name='用户唯一ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 27, 18, 23, 51, 602801), verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('2', '女'), ('1', '男')], default='1', max_length=10, verbose_name='性别'),
        ),
    ]
