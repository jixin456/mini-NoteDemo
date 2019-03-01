from django.db import models
from datetime import datetime
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProFile(AbstractUser):

    '''
    用户表
    '''

    Gender = {
        ('1','男'),
        ('2','女'),
    }

    openid = models.CharField(max_length=200,default='',verbose_name='用户微信唯一ID') #微信后台服务器提供唯一ID
    user_id = models.CharField(max_length=50,default=uuid4().hex,unique=True,verbose_name='用户唯一ID')

    nick_name = models.CharField(max_length=20,verbose_name='用户微信昵称')
    gender = models.CharField(max_length=10,choices=Gender,default='1',verbose_name='性别')
    avatarUrl = models.URLField(max_length=500,default='',verbose_name='用户微信头像url')
    country = models.CharField(max_length=100,default='',verbose_name='用户微信国家')
    province = models.CharField(max_length=100,default='',verbose_name='用户微信省份')
    city = models.CharField(max_length=100,default='',verbose_name='用户微信城市')
    language = models.CharField(max_length=100,default='',verbose_name='用户微信语言')

    add_time = models.DateTimeField(default=datetime.now(),verbose_name='注册时间')

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name