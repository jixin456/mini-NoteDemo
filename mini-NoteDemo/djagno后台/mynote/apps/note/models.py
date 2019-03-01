# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class NoteModel(models.Model):

    user = models.ForeignKey(USER,verbose_name='用户',on_delete=False)
    content = models.TextField(max_length=500,verbose_name='便签内容')

    class Meta:
        verbose_name = '便签管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content