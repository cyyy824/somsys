from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=120, verbose_name="部门名称")

    def __str__(self):
        return self.name

class OAUser(AbstractUser):
    realname = models.CharField('姓名', max_length=100)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    source = models.CharField("创建来源", max_length=100, blank=True)

    department = models.ForeignKey("Department", on_delete=models.CASCADE,related_name='users',verbose_name="部门")

    def __str__(self):
        return self.realname
