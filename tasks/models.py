from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import django.utils.timezone as timezone

# Create your models here.

'''
class Task(models.Model):

    name = models.CharField(max_length=128, verbose_name=u'任务名')

    progress = models.IntegerField(default=0, validators=[MaxValueValidator(
        100), MinValueValidator(0)], verbose_name=u'进度')

    transactor = models.CharField(max_length=32, verbose_name=u'办理人')

    content = models.TextField(blank=True, verbose_name=u'内容说明')

    parent_task = models.ForeignKey(
        'Task', on_delete=models.SET_NULL, related_name='child_projects', blank=True, null=True, verbose_name=u'父任务')

    department = models.ForeignKey(
        "accounts.Department", on_delete=models.CASCADE, related_name='projects', verbose_name=u'部门')

    cuser = models.ForeignKey(
        'accounts.OAUser', on_delete=models.SET_NULL, related_name='create_projects', blank=True, null=True)
    lcuser = models.ForeignKey(
        'accounts.OAUser', on_delete=models.SET_NULL, related_name='change_projects', blank=True, null=True)

    cdate = models.DateTimeField(default=timezone.now, verbose_name=u'创建日期')
    lcdate = models.DateTimeField(auto_now=True, verbose_name=u'修改日期')
    remark = models.CharField(max_length=256, blank=True)
'''
