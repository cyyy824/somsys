from django.db import models
import django.utils.timezone as timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class BudgetYear(models.Model):
    year = models.DecimalField(max_digits=4, unique=True, decimal_places=0)

    def __str__(self):
        return str(self.year)

    def __repr__(self):
        return str(self.year)


class Budget(models.Model):

    BUSINESSENTITY_CHOICES = (
        (u'集团', u'集团'),
        (u'管委会', u'管委会')
    )

    name = models.CharField(max_length=128)
    businessentity = models.CharField(
        max_length=6, choices=BUSINESSENTITY_CHOICES, default=u'集团')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    cdate = models.DateTimeField(default=timezone.now)
    lcdate = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=256, blank=True)

    cuser = models.ForeignKey('accounts.OAUser', on_delete=models.SET_NULL,
                              related_name='create_budgets', blank=True, null=True)
    lcuser = models.ForeignKey('accounts.OAUser', on_delete=models.SET_NULL,
                               related_name='change_budgets', blank=True, null=True)

    year = models.ForeignKey('BudgetYear', on_delete=models.SET_NULL,
                             related_name='budgets', blank=True, null=True)

    department = models.ForeignKey(
        "accounts.Structure", on_delete=models.CASCADE, related_name='budgets', verbose_name="部门")

    def __str__(self):
        return repr(self.year)+'-'+self.businessentity+'-'+self.name

    def __repr__(self):
        return repr(self.year)+'-'+self.businessentity+'-'+self.name


class Pay(models.Model):

    BUSINESSENTITY_CHOICES = (
        (u'集团', u'集团'),
        (u'管委会', u'管委会')
    )

    name = models.CharField(max_length=128)
    businessentity = models.CharField(
        max_length=6, choices=BUSINESSENTITY_CHOICES)
    paydate = models.DateTimeField(default=timezone.now)
    # transactor = models.CharField(max_length=32)
    transactor = models.ForeignKey(
        'accounts.OAUser', on_delete=models.CASCADE, related_name='transactor_pays', blank=True, null=True, verbose_name='经办人')

    amount = models.DecimalField(max_digits=11, decimal_places=2)
    remark = models.CharField(max_length=256, blank=True)

    cuser = models.ForeignKey(
        'accounts.OAUser', on_delete=models.SET_NULL, related_name='create_pays', blank=True, null=True)
    lcuser = models.ForeignKey(
        'accounts.OAUser', on_delete=models.SET_NULL, related_name='change_pays', blank=True, null=True)

    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL, related_name='pays', blank=True, null=True)
    budget = models.ForeignKey(
        'Budget', on_delete=models.SET_NULL, related_name='pays', blank=True, null=True)

    department = models.ForeignKey(
        "accounts.Structure", on_delete=models.CASCADE, related_name='pays', verbose_name="部门")

    def __str__(self):
        return self.name

# pay change or add, update project change time


@receiver(post_save, sender=Pay)
def change_schedule(sender, instance, created, **kwargs):
    if instance:
        project = instance.project
        if project:
            project.lcdate = timezone.now
            project.save()
