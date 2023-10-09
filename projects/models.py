from django.db import models
import django.utils.timezone as timezone
# from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

User = get_user_model()


class Project(models.Model):

    BUSINESSENTITY_CHOICES = (
        (u'集团', u'集团'),
        (u'管委会', u'管委会')
    )

    TASK_STATE_CHOICES = (
        (u'前期', u'前期'),
        (u'设计', u'设计'),
        (u'招标', u'招标'),
        (u'合同流程', u'合同流程'),
        (u'实施', u'实施'),
        (u'验收完成', u'验收完成'),
        (u'完成', u'完成'),
        (u'暂停', u'暂停'),
        (u'其他', u'其他')
    )

    name = models.CharField(max_length=128, verbose_name='项目名')
    businessentity = models.CharField(
        max_length=6, choices=BUSINESSENTITY_CHOICES, default='集团', verbose_name='主体')
    task_state = models.CharField(
        max_length=20, choices=TASK_STATE_CHOICES, default='其他', verbose_name='状态')
    transactor = models.CharField(max_length=32, verbose_name='经办人')
    amount = models.DecimalField(
        max_digits=11, decimal_places=2, verbose_name='金额', default=0)
    content = models.TextField(blank=True, verbose_name='内容简介')
    cdate = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    lcdate = models.DateTimeField(auto_now=True, verbose_name='修改日期')
    remark = models.CharField(max_length=256, blank=True, verbose_name='备注')

    cuser = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='create_projects', blank=True, null=True, verbose_name='创建人')
    lcuser = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='change_projects', blank=True, null=True, verbose_name='最后修改人')

    parent_project = models.ForeignKey(
        'Project', on_delete=models.SET_NULL, related_name='child_projects', blank=True, null=True, verbose_name='父项目')

    department = models.ForeignKey(
        "accounts.Structure", on_delete=models.CASCADE, related_name='projects', verbose_name="部门")

    def __str__(self):
        return self.name


class Schedule(models.Model):

    TASK_TYPE_CHOICES = (
        (u'进度', u'进度'),
        (u'付款', u'付款'),
        (u'会议', u'会议'),
        (u'流程', u'流程'),
        (u'发文', u'发文'),
        (u'招采审核', u'招采审核'),
        (u'方案评审会', u'方案评审会'),
        (u'其他', u'其他')
    )

    name = models.CharField(max_length=128, verbose_name='事项')
    cdate = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    lcdate = models.DateTimeField(auto_now=True, verbose_name='修改日期')

    task_type = models.CharField(
        max_length=20, choices=TASK_TYPE_CHOICES, null=True, verbose_name='类型')

    transactor = models.CharField(max_length=32, verbose_name='经办人')
    content = models.TextField(blank=True, verbose_name='内容')

    iskey = models.BooleanField(default=False, verbose_name=u'是否关键节点')
    isfin = models.BooleanField(default=False, verbose_name=u'是否完成')
    progress = models.IntegerField(default=0, validators=[MaxValueValidator(
        100), MinValueValidator(0)], verbose_name=u'进度占比')

    deadline = models.DateTimeField(null=True, verbose_name='截止日期')

    remark = models.CharField(max_length=256, blank=True, verbose_name='备注')

    cuser = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='create_schedules', blank=True, null=True, verbose_name='')
    lcuser = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='change_schedules', blank=True, null=True, verbose_name='')

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='schedules', verbose_name='')

    department = models.ForeignKey(
        "accounts.Structure", on_delete=models.CASCADE, verbose_name="部门")

    def is_expired(self):
        if self.deadline:
            if not self.isfin and timezone.now() > self.deadline:
                return True
        return False

    def __str__(self):
        return self.name


@receiver(post_save, sender=Schedule)
def change_schedule(sender, instance, created, **kwargs):
    if instance:
        project = instance.project
        project.lcdate = timezone.now
        project.save()
