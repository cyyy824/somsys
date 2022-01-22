from django.db import models
import django.utils.timezone as timezone

# Create your models here.
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
        (u'完结', u'完结'),
        (u'暂停', u'暂停')
    )

    name = models.CharField(max_length=128)
    businessentity = models.CharField(max_length=6,choices=BUSINESSENTITY_CHOICES)
    task_state = models.CharField(max_length=10,choices=TASK_STATE_CHOICES)
    transactor = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=11,decimal_places=2)
    cdate = models.DateTimeField(default = timezone.now)
    lcdate = models.DateTimeField(auto_now = True)
    remark = models.CharField(max_length=256,blank=True)

    parent_project = models.ForeignKey('Project', on_delete=models.SET_NULL,related_name='child_projects',blank = True, null=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):

    name = models.CharField(max_length=128)
    cdate = models.DateTimeField(default = timezone.now)
    lcdate = models.DateTimeField(auto_now = True)

    transactor = models.CharField(max_length=32)
    content = models.TextField(blank=True)

    remark = models.CharField(max_length=256,blank=True)

    project = models.ForeignKey('Project', on_delete=models.CASCADE ,related_name='schedules')

    def __str__(self):
        return self.name