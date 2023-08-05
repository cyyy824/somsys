from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.


class OAUser(AbstractUser):
    realname = models.CharField('姓名', max_length=100)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    source = models.CharField("创建来源", max_length=100, blank=True)

    department = models.ForeignKey(
        "Structure", null=True, on_delete=models.SET_NULL, related_name='users', verbose_name="部门")

    def __str__(self):
        return self.realname


class Structure(models.Model):
    """
    组织架构
    """
    type_choices = (("firm", "公司"), ("department", "部门"))
    title = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(
        max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, blank=True, verbose_name="父类架构")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
